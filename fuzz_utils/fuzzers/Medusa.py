""" Generates a test file from Medusa reproducers """
from typing import Any, NoReturn
import jinja2

from slither import Slither
from slither.core.declarations.contract import Contract
from slither.core.declarations.function_contract import FunctionContract
from slither.core.solidity_types.elementary_type import ElementaryType
from slither.core.solidity_types.user_defined_type import UserDefinedType
from slither.core.solidity_types.array_type import ArrayType
from slither.core.declarations.structure import Structure
from slither.core.declarations.structure_contract import StructureContract
from slither.core.declarations.enum import Enum
from slither.core.declarations.enum_contract import EnumContract
from fuzz_utils.utils.crytic_print import CryticPrint
from fuzz_utils.templates.foundry_templates import templates
from fuzz_utils.utils.encoding import parse_medusa_byte_string
from fuzz_utils.utils.error_handler import handle_exit


class Medusa:
    """
    Handles the generation of Foundry test files from Medusa reproducers
    """

    def __init__(self, target_name: str, corpus_path: str, slither: Slither) -> None:
        self.name = "Medusa"
        self.target_name = target_name
        self.corpus_path = corpus_path
        self.slither = slither
        self.target = self.get_target_contract()
        self.reproducer_dir = f"{corpus_path}/test_results"

    def get_target_contract(self) -> Contract:
        """Finds and returns Slither Contract"""
        contracts = self.slither.get_contract_from_name(self.target_name)
        # Loop in case slither fetches multiple contracts for some reason (e.g., similar names?)
        for contract in contracts:
            if contract.name == self.target_name:
                return contract

        handle_exit(f"\n* Slither could not find the specified contract `{self.target_name}`.")

    def parse_reproducer(self, calls: Any, index: int) -> str:
        """
        Takes a list of call dicts and returns a Foundry unit test string containing the call sequence.
        """
        call_list = []
        end = len(calls) - 1
        function_name = ""
        for idx, call in enumerate(calls):
            call_str, fn_name = self._parse_call_object(call)
            call_list.append(call_str)
            if idx == end:
                function_name = fn_name + "_" + str(index)

        template = jinja2.Template(templates["TEST"])
        return template.render(function_name=function_name, call_list=call_list)
        # 1. Take a reproducer list and create a test file based on the name of the last function of the list e.g. test_auto_$function_name
        # 2. For each object in the list process the call object and add it to the call list
        # 3. Using the call list to generate a test string
        # 4. Return the test string

    def _parse_call_object(self, call_dict: dict) -> tuple[str, str]:
        """
        Takes a single call dictionary, parses it, and returns the series of function calls as a string, along with
        the name of the last function, which is used as the name of the test.
        """
        # 1. Parse call object and save the variables
        time_delay = int(call_dict["blockTimestampDelay"])
        block_delay = int(call_dict["blockNumberDelay"])
        has_delay = time_delay > 0 or block_delay > 0

        # TODO check how Medusa handles empty calls

        function_name = call_dict["call"]["dataAbiValues"]["methodName"]
        function_parameters = call_dict["call"]["dataAbiValues"]["inputValues"]
        if len(function_parameters) == 0:
            function_parameters = ""
        caller = call_dict["call"]["from"]
        value = int(call_dict["call"]["value"], 16)

        slither_entry_point: FunctionContract

        for entry_point in self.target.functions_entry_points:
            if entry_point.name == function_name:
                slither_entry_point = entry_point

        if "slither_entry_point" not in locals():
            handle_exit(
                f"\n* Slither could not find the function `{function_name}` specified in the call object"
            )

        # 2. Decode the function parameters
        variable_definition, call_definition = self._decode_function_params(
            function_parameters, False, slither_entry_point
        )

        # 3. Generate a call string and return it
        template = jinja2.Template(templates["CALL"])
        call_str = template.render(
            has_delay=has_delay,
            time_delay=time_delay,
            block_delay=block_delay,
            caller=caller,
            value=value,
            function_parameters=", ".join(call_definition),
            function_name=function_name,
            contract_name=self.target_name,
        )
        # If we need to define local variables, append them to the call sequence
        if variable_definition is not None:
            call_str = variable_definition + call_str

        return call_str, function_name

    # pylint: disable=R0201
    def _match_elementary_types(self, param: str, recursive: bool, input_parameter: Any) -> str:
        """
        Returns a string which represents a elementary type literal value. e.g. "5" or "uint256(5)"

                Parameters:
                        param (dict): A dictionary containing information about the function parameter
                        recursive (int): A boolean, determining if the elementary type should be casted
                                         e.g., "uint256(5)", or returned as is, e.g., "5".

                Returns:
                        (str): String of the input parameter literal
        """
        input_type = input_parameter.type

        if "bool" in input_type:
            return param.lower()
        if "int" in input_type:
            if not recursive:
                return param
            return f"{input_type}({param})"
        if "bytes" in input_type:
            # Haskell encoding needs to be stripped and then converted to a hex literal
            literal_bytes = f'{input_type}(hex"{param}")'
            return literal_bytes
        if "string" in input_type:
            hex_string = parse_medusa_byte_string(param)
            interpreted_string = f'string(hex"{hex_string}")'
            return interpreted_string
        if "address" in input_type:
            return param

        handle_exit(
            f"\n* The parameter type `{input_type}` could not be found in the call object. This could indicate an issue in decoding the call sequence, or a missing feature. Please open an issue at https://github.com/crytic/fuzz-utils/issues"
        )

    def _match_array_type(
        self, param: dict, index: int, input_parameter: Any
    ) -> tuple[str, str, int]:
        # TODO check if fixed arrays are considered dynamic or not
        dynamic = input_parameter.is_dynamic_array
        if not dynamic:
            # Fixed array
            _, func_params = self._decode_function_params(param, True, input_parameter)
            return f"[{','.join(func_params)}]", "", index

        # Dynamic arrays
        # Consider cases where the array items are more complex types (bytes, string, tuples)
        definitions, func_params = self._decode_function_params(param, True, input_parameter)
        name, var_def = self._get_memarr(param, index, input_parameter)
        definitions += var_def

        for idx, temp_param in enumerate(func_params):
            definitions += "\t\t" + name + f"[{idx}] = {temp_param};\n"
        index += 1

        return name, definitions, index

    def _match_user_defined_type(
        self, param: list[Any] | dict[Any, Any], input_parameter: Any
    ) -> tuple[str, str]:
        match input_parameter.type:
            case Structure() | StructureContract():  # type: ignore[misc]
                definitions, func_params = self._decode_function_params(  # type: ignore[unreachable]
                    param, True, input_parameter.type.elems_ordered
                )
                return definitions, f"{input_parameter}({','.join(func_params)})"
            case Enum() | EnumContract():  # type: ignore[misc]
                return "", f"{input_parameter}({param})"  # type: ignore[unreachable]
            case _:
                handle_exit(
                    f"\n* The parameter type `{input_parameter.type}` could not be found in the call object. This could indicate an issue in decoding the call sequence, or a missing feature. Please open an issue at https://github.com/crytic/fuzz-utils/issues"
                )

    def _decode_function_params(
        self, function_params: list | dict, recursive: bool, entry_point: Any
    ) -> tuple[str, list] | NoReturn:
        params = []
        variable_definitions = ""
        index = 0
        # 1. Get a list of function parameters in hex, and their types
        # 2. Decode the types and add to the input list
        if isinstance(function_params, dict):
            # This should only ever be the case when the parameter is a struct
            for var in entry_point:
                input_parameter = var.type
                input_value = function_params[var.name]

                match input_parameter:
                    case ElementaryType():  # type: ignore[misc]
                        params.append(  # type: ignore[unreachable]
                            self._match_elementary_types(
                                str(input_value), recursive, input_parameter
                            )
                        )
                    case ArrayType():  # type: ignore[misc]
                        [inputs, definitions, index] = self._match_array_type(  # type: ignore[unreachable]
                            input_value, index, input_parameter
                        )
                        params.append(inputs)
                        variable_definitions += definitions
                    case UserDefinedType():  # type: ignore[misc]
                        definitions, func_params = self._match_user_defined_type(  # type: ignore[unreachable, unpacking-non-sequence]
                            input_value, input_parameter
                        )
                        variable_definitions += definitions
                        params.append(func_params)
                    case _:
                        # TODO should handle all cases, but keeping this just in case
                        CryticPrint().print_information(
                            f"\n* Attempted to decode an unidentified type {input_parameter}, this call will be skipped. Please open an issue at https://github.com/crytic/fuzz-utils/issues"
                        )
                        continue
        else:
            for param_idx, param in enumerate(function_params):
                input_parameter = None
                if recursive:
                    if isinstance(entry_point, list):
                        input_parameter = entry_point[param_idx].type
                    else:
                        input_parameter = entry_point.type

                else:
                    input_parameter = entry_point.parameters[param_idx].type

                match input_parameter:
                    case ElementaryType():  # type: ignore[misc]
                        params.append(  # type: ignore[unreachable]
                            self._match_elementary_types(str(param), recursive, input_parameter)
                        )
                    case ArrayType():  # type: ignore[misc]
                        inputs, definitions, index = self._match_array_type(  # type: ignore[unreachable]
                            param, index, input_parameter
                        )
                        params.append(inputs)
                        variable_definitions += definitions
                    case UserDefinedType():  # type: ignore[misc]
                        definitions, func_params = self._match_user_defined_type(  # type: ignore[unreachable, unpacking-non-sequence]
                            param, input_parameter
                        )
                        variable_definitions += definitions
                        params.append(func_params)
                    case _:
                        # TODO should handle all cases, but keeping this just in case
                        CryticPrint().print_information(
                            f"\n* Attempted to decode an unidentified type {input_parameter}, this call will be skipped. Please open an issue at https://github.com/crytic/fuzz-utils/issues"
                        )
                        continue

        # 3. Return a list of function parameters
        if len(variable_definitions) > 0:
            return variable_definitions, params

        return "", params

    # pylint: disable=R0201
    def _get_memarr(
        self, function_params: dict | list, index: int, input_parameter: Any
    ) -> tuple[str, str]:
        length = len(function_params)

        input_type = input_parameter.type
        name = f"dyn{input_type}Arr_{index}"
        declaration = f"{input_type}[] memory {name} = new {input_type}[]({length});\n"
        return name, declaration
