""" Generates a test file from Echidna reproducers """
# type: ignore[misc] # Ignores 'Any' input parameter
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
from fuzz_utils.utils.crytic_print import CryticPrint
from fuzz_utils.templates.foundry_templates import templates
from fuzz_utils.utils.encoding import parse_echidna_byte_string
from fuzz_utils.utils.error_handler import handle_exit


class Echidna:
    """
    Handles the generation of Foundry test files from Echidna reproducers
    """

    def __init__(self, target_name: str, corpus_path: str, slither: Slither) -> None:
        self.name = "Echidna"
        self.target_name = target_name
        self.slither = slither
        self.target = self.get_target_contract()
        self.reproducer_dir = f"{corpus_path}/reproducers"

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
        # 1. For each object in the list process the call object and add it to the call list
        for idx, call in enumerate(calls):
            call_str, fn_name = self._parse_call_object(call)
            call_list.append(call_str)
            if idx == end:
                function_name = fn_name + "_" + str(index)

        # 2. Generate the test string and return it
        template = jinja2.Template(templates["TEST"])
        return template.render(function_name=function_name, call_list=call_list)

    def _parse_call_object(self, call_dict: dict[Any, Any]) -> tuple[str, str]:
        """
        Takes a single call dictionary, parses it, and returns the series of function calls as a string, along with
        the name of the last function, which is used as the name of the test.
        """
        # 1. Parse call object and save the variables
        time_delay = int(call_dict["delay"][0], 16)
        block_delay = int(call_dict["delay"][1], 16)
        has_delay = time_delay > 0 or block_delay > 0
        value = int(call_dict["value"], 16)
        caller = call_dict["src"]

        if call_dict["call"]["tag"] == "NoCall":
            template = jinja2.Template(templates["EMPTY"])
            call_str = template.render(time_delay=time_delay, block_delay=block_delay)
            return (call_str, "")

        function_name = call_dict["call"]["contents"][0]

        if not function_name:
            template = jinja2.Template(templates["TRANSFER"])
            call_str = template.render(
                time_delay=time_delay, block_delay=block_delay, value=value, caller=caller
            )
            return (call_str, "")

        function_parameters = call_dict["call"]["contents"][1]
        if len(function_parameters) == 0:
            function_parameters = ""

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
    def _match_elementary_types(self, param: dict, recursive: bool) -> str | NoReturn:
        """
        Returns a string which represents a elementary type literal value. e.g. "5" or "uint256(5)"

                Parameters:
                        param (dict): A dictionary containing information about the function parameter
                        recursive (int): A boolean, determining if the elementary type should be casted
                                         e.g., "uint256(5)", or returned as is, e.g., "5".

                Returns:
                        (str): String of the input parameter literal
        """
        match param["tag"]:
            case "AbiBool":
                # Represented as True or False, needs to be lowercased to work
                return str(param["contents"]).lower()
            case "AbiUInt" | "AbiInt":
                # The numbers are represented as [format (e.g., 8 for uint8), "number" (string of number)]
                # So I can just append the second element string
                cast = "uint" if param["tag"] == "AbiUInt" else "int"
                if not recursive:
                    return param["contents"][1]

                casting = f'{cast}{str(param["contents"][0])}({param["contents"][1]})'
                return casting
            case "AbiAddress":
                return param["contents"]
            case "AbiBytes" | "AbiBytesDynamic":
                is_fixed_size = isinstance(param["contents"], list)
                size = param["contents"][0] if is_fixed_size else ""
                contents = param["contents"][1] if is_fixed_size else param["contents"]

                # Haskell encoding needs to be stripped and then converted to a hex literal
                hex_string = parse_echidna_byte_string(contents.strip('"'))
                interpreted_string = f'hex"{hex_string}"'
                if not recursive:
                    result = (
                        f"bytes{size}({interpreted_string})"
                        if is_fixed_size
                        else interpreted_string
                    )
                    return result

                casting = f"bytes{size}({interpreted_string})"
                return casting
            case "AbiString":
                hex_string = parse_echidna_byte_string(param["contents"].strip('"'))
                interpreted_string = f'string(hex"{hex_string}")'
                return interpreted_string
            case _:
                handle_exit(
                    f"\n* The parameter tag `{param['tag']}` could not be found in the call object. This could indicate an issue in decoding the call sequence, or a missing feature. Please open an issue at https://github.com/crytic/fuzz-utils/issues"
                )

    def _match_array_type(
        self, param: dict, index: int, input_parameter: Any
    ) -> tuple[str, str, int] | NoReturn:
        match param["tag"]:
            case "AbiArray":
                # Consider cases where the array items are more complex types (bytes, string, tuples)
                _, func_params = self._decode_function_params(
                    param["contents"][2], True, input_parameter
                )
                return f"[{','.join(func_params)}]", "", index
            case "AbiArrayDynamic":
                # Consider cases where the array items are more complex types (bytes, string, tuples)
                definitions, func_params = self._decode_function_params(
                    param["contents"][1], True, input_parameter
                )
                name, var_def = self._get_memarr(param["contents"], index, input_parameter)  # type: ignore[unpacking-non-sequence]
                definitions += var_def

                for idx, temp_param in enumerate(func_params):
                    definitions += f"\t\t{name}[{idx}] = {temp_param};\n"
                index += 1

                return name, definitions, index
            case _:
                handle_exit(
                    f"\n* The parameter tag `{param['tag']}` could not be found in the call object. This could indicate an issue in decoding the call sequence, or a missing feature. Please open an issue at https://github.com/crytic/fuzz-utils/issues"
                )

    def _match_user_defined_type(
        self, param: dict, input_parameter: Any
    ) -> tuple[str, str] | NoReturn:
        match param["tag"]:
            case "AbiTuple":
                match input_parameter.type:
                    case Structure() | StructureContract():  # type: ignore[misc]
                        definitions, func_params = self._decode_function_params(  # type: ignore[unreachable]
                            param["contents"], True, input_parameter.type.elems_ordered
                        )
                        return definitions, f"{input_parameter}({','.join(func_params)})"
                    case _:
                        handle_exit(
                            f"\n* The parameter type `{input_parameter.type}` could not be found. This could indicate an issue in decoding the call sequence, or a missing feature. Please open an issue at https://github.com/crytic/fuzz-utils/issues"
                        )
            case "AbiUInt":
                if isinstance(input_parameter.type, Enum):
                    enum_uint = self._match_elementary_types(param, False)
                    return "", f"{input_parameter}({enum_uint})"

                # TODO is this even reachable?
                handle_exit(
                    f"\n* The parameter type `{input_parameter.type}` does not match the intended type `Enum`. This could indicate an issue in decoding the call sequence, or a missing feature. Please open an issue at https://github.com/crytic/fuzz-utils/issues"
                )
            case _:
                handle_exit(
                    f"\n* The parameter tag `{param['tag']}` could not be found in the call object. This could indicate an issue in decoding the call sequence, or a missing feature. Please open an issue at https://github.com/crytic/fuzz-utils/issues"
                )

    def _decode_function_params(
        self, function_params: list, recursive: bool, entry_point: Any
    ) -> tuple[str, list]:
        params = []
        variable_definitions = ""
        index = 0
        # 1. Get a list of function parameters in hex, and their types
        # 2. Decode the types and add to the input list
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
                    params.append(self._match_elementary_types(param, recursive))  # type: ignore[unreachable]
                case ArrayType():  # type: ignore[misc]
                    inputs, definitions, new_index = self._match_array_type(  # type: ignore[unreachable,unpacking-non-sequence]
                        param, index, input_parameter
                    )
                    params.append(inputs)
                    variable_definitions += definitions
                    index = new_index
                case UserDefinedType():  # type: ignore[misc]
                    definitions, func_params = self._match_user_defined_type(param, input_parameter)  # type: ignore[unreachable, unpacking-non-sequence]
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
        self, function_params: dict, index: int, input_parameter: Any
    ) -> tuple[str, str]:
        length = len(function_params[1])

        input_type = input_parameter.type
        name = f"dyn{input_type}Arr_{index}"
        declaration = f"{input_type}[] memory {name} = new {input_type}[]({length});\n"
        return name, declaration
