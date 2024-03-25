""" Generates a test file from Medusa reproducers """
from typing import Any
import jinja2
from eth_abi import abi
from eth_utils import to_checksum_address
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
from fuzz_utils.templates.foundry_templates import templates
from fuzz_utils.utils.encoding import byte_to_escape_sequence
from fuzz_utils.utils.error_handler import handle_exit


class Medusa:  # pylint: disable=too-many-instance-attributes
    """
    Handles the generation of Foundry test files from Medusa reproducers
    """

    def __init__(
        self, target_name: str, corpus_path: str, slither: Slither, named_inputs: bool
    ) -> None:
        self.name = "Medusa"
        self.target_name = target_name
        self.corpus_path = corpus_path
        self.slither = slither
        self.target = self.get_target_contract()
        self.reproducer_dir = f"{corpus_path}/test_results"
        self.corpus_dirs = [
            f"{corpus_path}/call_sequences/immutable",
            f"{corpus_path}/call_sequences/mutable",
            self.reproducer_dir,
        ]
        self.named_inputs = named_inputs

    def get_target_contract(self) -> Contract:
        """Finds and returns Slither Contract"""
        contracts = self.slither.get_contract_from_name(self.target_name)
        # Loop in case slither fetches multiple contracts for some reason (e.g., similar names?)
        for contract in contracts:
            if contract.name == self.target_name:
                return contract

        handle_exit(f"\n* Slither could not find the specified contract `{self.target_name}`.")

    def parse_reproducer(self, file_path: str, calls: Any, index: int) -> str:
        """
        Takes a list of call dicts and returns a Foundry unit test string containing the call sequence.
        """
        call_list = []
        end = len(calls) - 1
        function_name = ""
        has_low_level_call: bool = False

        for idx, call in enumerate(calls):
            call_str, fn_name = self._parse_call_object(call)
            call_list.append(call_str)
            has_low_level_call = has_low_level_call or ("(success, " in call_str)
            if idx == end:
                function_name = fn_name + "_" + str(index)

        template = jinja2.Template(templates["TEST"])
        return template.render(
            function_name=function_name,
            call_list=call_list,
            file_path=file_path,
            has_low_level_call=has_low_level_call,
        )
        # 1. Take a reproducer list and create a test file based on the name of the last function of the list e.g. test_auto_$function_name
        # 2. For each object in the list process the call object and add it to the call list
        # 3. Using the call list to generate a test string
        # 4. Return the test string

    # pylint: disable=too-many-locals,too-many-branches
    def _parse_call_object(self, call_dict: dict) -> tuple[str, str]:
        """
        Takes a single call dictionary, parses it, and returns the series of function calls as a string, along with
        the name of the last function, which is used as the name of the test.
        """
        # 1. Parse call object and save the variables
        time_delay = int(call_dict["blockTimestampDelay"])
        block_delay = int(call_dict["blockNumberDelay"])
        value = int(call_dict["call"]["value"], 16)
        has_delay = time_delay > 0 or block_delay > 0
        function_name: str = ""

        # @note Medusa has no concept of empty calls
        # @note Added to support Medusa <=0.1.3
        if "methodName" in call_dict["call"]["dataAbiValues"]:
            function_name = call_dict["call"]["dataAbiValues"]["methodName"]
        elif "methodSignature" in call_dict["call"]["dataAbiValues"]:
            function_name = call_dict["call"]["dataAbiValues"]["methodSignature"].split("(")[0]
        else:
            handle_exit(
                "There was an issue parsing the Medusa call sequences. This indicates a breaking change in the call sequence format, please open an issue at https://github.com/crytic/fuzz-utils/issues"
            )

        function_parameters = call_dict["call"]["dataAbiValues"]["inputValues"]
        data = call_dict["call"]["data"]
        data_bytes = bytes.fromhex(data[10:]) if len(data) > 10 else b""

        if len(function_parameters) == 0:
            function_parameters = ""
        caller = call_dict["call"]["from"]

        slither_entry_point: FunctionContract

        for entry_point in self.target.functions_entry_points:
            if entry_point.name == function_name:
                slither_entry_point = entry_point

        if "slither_entry_point" not in locals():
            handle_exit(
                f"\n* Slither could not find the function `{function_name}` specified in the call object"
            )

        if not slither_entry_point.payable:
            value = 0

        # 2. Decode the function parameters
        parameters: list = []
        variable_definition: str = ""

        if len(data_bytes) > 0 and len(slither_entry_point.parameters) > 0:
            types, _, _ = self._get_types_signature(slither_entry_point.parameters, None)
            # Nested tuple
            decoded = abi.decode(types, data_bytes)
            _, func_params, variable_definition = self._get_types_signature(
                slither_entry_point.parameters, decoded
            )
            parameters.extend(func_params)

        parameters_str: str = ""
        if isinstance(slither_entry_point.parameters, list):
            if self.named_inputs and len(slither_entry_point.parameters) > 0:
                for idx, input_param in enumerate(slither_entry_point.parameters):
                    parameters[idx] = input_param.name + ": " + parameters[idx]
                parameters_str = "{" + ", ".join(parameters) + "}"
            else:
                parameters_str = ", ".join(parameters)

        # 3. Generate a call string and return it
        template = jinja2.Template(templates["CALL"])
        call_str = template.render(
            has_delay=has_delay,
            time_delay=time_delay,
            block_delay=block_delay,
            caller=caller,
            value=value,
            function_parameters=parameters_str,
            function_name=function_name,
            contract_name=self.target_name,
        )
        # If we need to define local variables, append them to the call sequence
        if variable_definition is not None:
            call_str = variable_definition + call_str

        return call_str, function_name

    def _get_types_signature(
        self, parameters: list, decoded_values: tuple | None
    ) -> tuple[list, list, str]:
        types: list[str] = []
        wrapped_parameters: list[str] = []
        var_definitions: str = ""

        for idx, parameter in enumerate(parameters):
            value = None
            if decoded_values:
                value = decoded_values[idx]

            (abi_type, param_value, var_def) = self._match_type(parameter, value)
            types.append(abi_type)
            wrapped_parameters.append(param_value)
            var_definitions += var_def
        return (types, wrapped_parameters, var_definitions)

    def _match_type(self, parameter: Any, values: Any) -> tuple[str, str, str]:
        abi_type: str = ""
        param_value: str = ""
        var_def: str = ""

        match parameter.type:
            case ElementaryType():  # type: ignore[misc]
                abi_type, param_value = process_elementary_type(parameter.type.type, values)  # type: ignore[unreachable]
            case ArrayType():  # type: ignore[misc]
                length = parameter.type.length if parameter.type.length else ""  # type: ignore[unreachable]
                matched_type, _, _ = self._match_type(parameter.type, None)
                abi_type = f"{matched_type}[{length}]"

                if parameter.type.is_dynamic_array:
                    # TODO make it work with multidim dynamic arrays
                    if values:
                        dyn_length = len(values)

                        array_type: str = ""
                        if isinstance(
                            parameter.type.type,
                            (Structure | StructureContract | Enum | EnumContract),
                        ):
                            array_type = parameter.type.type.name
                        else:
                            array_type = parameter.type.type
                        var_def += f"{array_type}[] memory {parameter.name} = new {parameter.type.type}[]({dyn_length});\n"

                        for idx, value in enumerate(values):
                            _, matched_value, _ = self._match_type(parameter.type, value)
                            var_def += f"        {parameter.name}[{idx}] = {matched_value};\n"
                        param_value = parameter.name
                else:
                    matched_values = []
                    if values:
                        for idx, value in enumerate(values):
                            _, matched_value, _ = self._match_type(parameter.type, value)
                            matched_values.append(matched_value)

                        param_value = f"[{','.join(matched_values)}]"
            case UserDefinedType():  # type: ignore[misc]
                match parameter.type.type:  # type: ignore[unreachable]
                    case Structure() | StructureContract():
                        matched_types = []
                        matched_values = []
                        for idx, struct_field in enumerate(parameter.type.type.elems_ordered):
                            value = None
                            if values:
                                value = values[idx]

                            field_type, field_value, field_definitions = self._match_type(
                                struct_field, value
                            )
                            var_def += field_definitions
                            matched_types.append(field_type)

                            if values:
                                matched_values.append(field_value)
                        abi_type = f"({','.join(matched_types)})"
                        param_value = f"{parameter.type}({','.join(matched_values)})"
                    case Enum() | EnumContract():
                        abi_type = "uint8"
                        if str(values):
                            param_value = f"{parameter.type}({values})"

        return (abi_type, param_value, var_def)


def process_elementary_type(parameter_type: str, values: Any) -> tuple[str, str]:
    """Returns the type for ABI decoding, and the literal value to populate unit tests"""
    abi_type: str = ""
    param_value: str = ""
    if parameter_type == "string":
        abi_type = "bytes"
    else:
        abi_type = parameter_type

    if values is not None:
        param_value = populate_parameter_value(parameter_type, values)

    return (abi_type, param_value)


def populate_parameter_value(parameter_type: str, values: Any) -> str:
    """Returns formatted value of the parameter based on type"""
    if parameter_type == "string":
        text = byte_to_escape_sequence(values)
        return f'unicode"{text}"'  # f'string(hex"{bytes.hex(values)}")'
    if "bytes" in parameter_type:
        return f'{parameter_type}(hex"{bytes.hex(values)}")'
    if parameter_type == "bool":
        return str(values).lower()
    if parameter_type == "address":
        return to_checksum_address(values)

    return f"{parameter_type}({values})"
