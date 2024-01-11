""" Generates a test file from Echidna reproducers """
import re
from typing import Any
import jinja2

from slither import Slither
from slither.core.declarations.contract import Contract
from slither.core.solidity_types.elementary_type import ElementaryType
from slither.core.solidity_types.user_defined_type import UserDefinedType
from slither.core.solidity_types.array_type import ArrayType
from slither.core.declarations.structure import Structure
from slither.core.declarations.structure_contract import StructureContract
from slither.core.declarations.enum import Enum
from test_generator.templates.foundry_templates import templates
from test_generator.utils.encoding import parse_echidna_byte_string


class Echidna:
    """
    Handles the generation of Foundry test files from Echidna reproducers
    """

    def __init__(self, target_name: str, corpus_path: str, slither: Slither) -> None:
        self.name = "Echidna"
        self.target_name = target_name
        self.slither = slither
        self.target = self._get_target_contract()
        self.reproducer_dir = f"{corpus_path}/reproducers"

    def _get_target_contract(self) -> Contract:
        contracts = self.slither.get_contract_from_name(self.target_name)
        # Loop in case slither fetches multiple contracts for some reason (e.g., similar names?)
        for contract in contracts:
            if contract.name == self.target_name:
                return contract

        # TODO throw error if no contract found
        exit(-1)

    def parse_reproducer(self, calls: list, index: int) -> str:
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

    def _parse_call_object(self, call_dict) -> (str, str):
        """
        Takes a single call dictionary, parses it, and returns the series of function calls as a string, along with
        the name of the last function, which is used as the name of the test.
        """
        # 1. Parse call object and save the variables
        time_delay = int(call_dict["delay"][0], 16)
        block_delay = int(call_dict["delay"][1], 16)
        has_delay = True if time_delay > 0 or block_delay > 0 else False

        if call_dict["call"]["tag"] == "NoCall":
            template = jinja2.Template(templates["EMPTY"])
            call_str = template.render(time_delay=time_delay, block_delay=block_delay)
            return (call_str, "")

        function_name = call_dict["call"]["contents"][0]
        function_parameters = call_dict["call"]["contents"][1]
        if len(function_parameters) == 0:
            function_parameters = ""
        caller = call_dict["src"]
        value = int(call_dict["value"], 16)

        slither_entry_point = None

        for entry_point in self.target.functions_entry_points:
            if entry_point.name == function_name:
                slither_entry_point = entry_point

        # 2. Decode the function parameters
        variable_definition, call_definition = self._decode_function_params(
            function_parameters, False, slither_entry_point
        )
        params = ", ".join(call_definition)

        # 3. Generate a call string and return it
        template = jinja2.Template(templates["CALL"])
        call_str = template.render(
            has_delay=has_delay,
            time_delay=time_delay,
            block_delay=block_delay,
            caller=caller,
            value=value,
            function_parameters=params,
            function_name=function_name,
            contract_name=self.target_name,
        )
        # If we need to define local variables, append them to the call sequence
        if variable_definition is not None:
            call_str = variable_definition + call_str

        return call_str, function_name

    def _match_elementary_types(self, param: dict, recursive: bool) -> str:
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
                else:
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
                else:
                    casting = f"bytes{size}({interpreted_string})"
                    return casting
            case "AbiString":
                hex_string = parse_echidna_byte_string(param["contents"].strip('"'))
                interpreted_string = f'string(hex"{hex_string}")'
                return interpreted_string

    def _match_array_type(self, param: dict, index: int, input_parameter) -> tuple[str, str, int]:
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
                name, var_def = self._get_memarr(param["contents"], index)
                definitions += var_def

                for idx, temp_param in enumerate(func_params):
                    definitions += f"\t\t{name}[{idx}] = {temp_param};\n"
                index += 1

                return name, definitions, index

    def _match_user_defined_type(self, param: dict, input_parameter) -> tuple[str, str]:
        match param["tag"]:
            case "AbiTuple":
                match input_parameter.type:
                    case Structure() | StructureContract():
                        definitions, func_params = self._decode_function_params(
                            param["contents"], True, input_parameter.type.elems_ordered
                        )
                        return definitions, f"{input_parameter}({','.join(func_params)})"
            case "AbiUInt":
                if isinstance(input_parameter.type, Enum):
                    enum_uint = self._match_elementary_types(param, False)
                    return "", f"{input_parameter}({enum_uint})"
                else:
                    # TODO is this even reachable?
                    return "", ""

    def _decode_function_params(
        self, function_params: list, recursive: bool, entry_point: Any
    ) -> (str | None, list):
        params = []
        variable_definitions = ""
        index = 0
        # 1. Get a list of function parameters in hex, and their types
        # 2. Decode the types and add to the input list
        for param_idx, param in enumerate(function_params):
            input_parameter = None
            if recursive:
                try:
                    input_parameter = entry_point[param_idx].type
                except:
                    input_parameter = entry_point.type

            else:
                input_parameter = entry_point.parameters[param_idx].type

            match input_parameter:
                case ElementaryType():
                    params.append(self._match_elementary_types(param, recursive))
                case ArrayType():
                    [inputs, definitions, new_index] = self._match_array_type(
                        param, index, input_parameter
                    )
                    params.append(inputs)
                    variable_definitions += definitions
                    index = new_index
                case UserDefinedType():
                    [definitions, func_params] = self._match_user_defined_type(
                        param, input_parameter
                    )
                    variable_definitions += definitions
                    params.append(func_params)
                case _:
                    # TODO should handle all cases, but keeping this just in case
                    print("UNHANDLED INPUT TYPE -> DEFAULT CASE")
                    continue

        # 3. Return a list of function parameters
        if len(variable_definitions) > 0:
            return variable_definitions, params
        else:
            return "", params

    def _get_memarr(self, function_params: dict, index: int) -> (str | None, str | None):
        length = len(function_params[1])
        match function_params[0]["tag"]:
            case "AbiBoolType":
                name = f"dynBoolArr_{index}"
                return name, f"bool[] memory {name} = new bool[]({length});\n"
            case "AbiIntType":
                name = f"dynIntArr_{index}"
                return (
                    name,
                    f"int{function_params[0]['contents']}[] memory {name} = new int{function_params[0]['contents']}[]({length});\n",
                )
            case "AbiUIntType":
                name = f"dynUintArr_{index}"
                return (
                    name,
                    f"uint{function_params[0]['contents']}[] memory {name} = new uint{function_params[0]['contents']}[]({length});\n",
                )
            case "AbiAddressType":
                name = f"dynAddressArr_{index}"
                return name, f"address[] memory {name} = new address[]({length});\n"
            case "AbiBytesType" | "AbiBytesDynamicType":
                name = f"dynBytesArr_{index}"
                return name, f"bytes[] memory {name} = new bytes[]({length});\n"
            case "AbiStringType":
                name = f"dynStringArr_{index}"
                return name, f"string[] memory {name} = new string[]({length});\n"
            case _:
                return None, None
