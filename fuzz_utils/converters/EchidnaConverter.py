""" Converts Echidna call sequences into the Medusa format"""
import os
import json
import copy
from typing import Any, NoReturn
from collections import defaultdict
from web3 import Web3

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

from fuzz_utils.utils.encoding import parse_echidna_byte_string
from fuzz_utils.utils.encoding import strip_hex_leading_zero
from fuzz_utils.utils.error_handler import handle_exit

# pylint: disable=too-many-instance-attributes
class EchidnaConverter:
    """Converts call sequences from a corpus into an Echidna or Medusa format"""

    __MEDUSA_CALL_FORMAT = {
        "call": {
            "from": "",
            "to": "",
            "nonce": 0,
            "value": "",
            "gasLimit": 12500000,
            "gasPrice": "0x1",
            "gasFeeCap": "0x0",
            "gasTipCap": "0x0",
            "data": "",
            "dataAbiValues": {"methodName": "", "inputValues": []},
            "AccessList": None,
            "SkipAccountChecks": False,
        },
        "blockNumberDelay": 0,
        "blockTimestampDelay": 0,
    }

    def __init__(
        self,
        target_name: str,
        corpus_path: str,
        gas_fee_cap: str,
        gas_tip_cap: str,
        slither: Slither,
        target_address: str,
        deployer: str,
    ) -> None:
        self.corpus_path = corpus_path
        self.gas_fee_cap = gas_fee_cap
        self.gas_tip_cap = gas_tip_cap
        self.slither = slither
        self.target_name = target_name
        self.target = self.get_target_contract()
        self.w3 = Web3(Web3.EthereumTesterProvider())
        self.contract = self.w3.eth.contract(
            abi=self.target.file_scope.abi(
                self.target.compilation_unit._crytic_compile_compilation_unit, self.target.name
            )
        )
        self.target_address = target_address
        self.deployer = deployer

    def convert(self) -> tuple[list, list, list, list]:
        """Parses corpus files and returns lists of converted files and file names"""
        converted_coverage = []
        converted_reproducers = []
        (
            coverage_list,
            reproducers_list,
            coverage_file_names,
            reproducers_file_names,
        ) = self._fetch_corpus()

        for coverage in coverage_list:
            single_file = self._parse_corpus_file(coverage)
            converted_coverage.append(single_file)

        for reproducer in reproducers_list:
            single_file = self._parse_corpus_file(reproducer)
            converted_reproducers.append(single_file)

        return (
            converted_coverage,
            converted_reproducers,
            coverage_file_names,
            reproducers_file_names,
        )

    def get_target_contract(self) -> Contract:
        """Finds and returns Slither Contract"""
        contracts = self.slither.get_contract_from_name(self.target_name)
        # Loop in case slither fetches multiple contracts for some reason (e.g., similar names?)
        for contract in contracts:
            if contract.name == self.target_name:
                return contract

        # TODO throw error if no contract found
        handle_exit(f"\n* Slither could not find the specified contract `{self.target_name}`.")

    def _parse_corpus_file(self, calls: list) -> list:
        users_nonces = defaultdict(lambda: 0)
        # NOTE: This is a hack to get around a Medusa error, won't work when deploying multiple contracts
        users_nonces[self.deployer] = 1
        medusa_call_list = []
        for _, call in enumerate(calls):
            _, call_str = self._parse_call_object(call, users_nonces)
            medusa_call_list.append(call_str)

        return medusa_call_list

    def _parse_call_object(self, call: dict, nonces: dict) -> tuple[dict, str]:
        """Converts a Echidna call dict into a Medusa call dict"""
        parsed_call: dict = copy.deepcopy(self.__MEDUSA_CALL_FORMAT)

        if call["call"]["tag"] == "NoCall":
            # TODO figure out how Medusa does empty calls
            return {}, ""
        # The sender, receiver, and value are encoded the same in both formats
        # So we can just copy it over to our template dict
        parsed_call["call"]["from"] = call["src"]
        parsed_call["call"]["to"] = self.target_address if self.target_address else call["dst"]
        parsed_call["call"]["value"] = strip_hex_leading_zero(call["value"])
        parsed_call["call"]["nonce"] = nonces[call["src"]]
        # Update sender nonce
        nonces[call["src"]] += 1
        parsed_call["call"]["gasLimit"] = call["gas"]
        parsed_call["call"]["gasPrice"] = strip_hex_leading_zero(call["gasprice"])
        # TODO check if these are the correct indexes
        parsed_call["blockTimestampDelay"] = int(call["delay"][0], 16)
        parsed_call["blockNumberDelay"] = int(call["delay"][1], 16)
        # Echidna does not have a concept of gasFeeCap and gasTipCap in the call sequences
        # Since these values seem to be configurable only once per campaign (i.e., they should be the same for the whole corpus)
        # we can safely use the default or make it configurable via CLI flags
        if self.gas_fee_cap:
            parsed_call["call"]["gasFeeCap"] = self.gas_fee_cap
        if self.gas_tip_cap:
            parsed_call["call"]["gasTipCap"] = self.gas_tip_cap
        # AccessList: null
        # SkipAccountChecks: false

        # dataAbiValues: {"methodName": "", "inputValues": []}
        method_name = call["call"]["contents"][0]
        parsed_call["call"]["dataAbiValues"]["methodName"] = method_name

        slither_entry_point: FunctionContract

        for entry_point in self.target.functions_entry_points:
            if entry_point.name == method_name:
                slither_entry_point = entry_point

        # Parse function input
        function_inputs = call["call"]["contents"][1]
        parsed_inputs = self._decode_function_params(function_inputs, False, slither_entry_point)
        parsed_call["call"]["dataAbiValues"]["inputValues"] = copy.deepcopy(parsed_inputs)

        _, types, _ = slither_entry_point.signature
        for idx, input_type in enumerate(types):
            if "bytes" in input_type:
                parsed_inputs[idx] = Web3.to_bytes(text=parsed_inputs[idx])

        parsed_call["call"]["data"] = self.contract.encodeABI(
            fn_name=method_name, args=parsed_inputs
        )

        return parsed_call, json.dumps(parsed_call)

    def _decode_function_params(
        self, function_params: list, recursive: bool, entry_point: Any
    ) -> list:
        params = []
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
                    params.append(self._match_elementary_types(param))  # type: ignore[unreachable]
                case ArrayType():  # type: ignore[misc]
                    inputs, new_index = self._match_array_type(  # type: ignore[unreachable,unpacking-non-sequence]
                        param, index, input_parameter
                    )
                    params.append(inputs)
                    index = new_index
                case UserDefinedType():  # type: ignore[misc]
                    func_params = self._match_user_defined_type(param, input_parameter)  # type: ignore[unreachable, unpacking-non-sequence]
                    params.append(func_params)
                case _:
                    # TODO should handle all cases, but keeping this just in case
                    CryticPrint().print_information(
                        f"\n* Attempted to decode an unidentified type {input_parameter}, this call will be skipped. Please open an issue at https://github.com/crytic/fuzz-utils/issues"
                    )
                    continue
        return params

    # pylint: disable=R0201
    def _match_elementary_types(self, param: dict) -> Any | NoReturn:
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
                return param["contents"]
            case "AbiUInt" | "AbiInt":
                # The numbers are represented as [format (e.g., 8 for uint8), "number" (string of number)]
                # So I can just append the second element string
                return int(param["contents"][1])
            case "AbiAddress":
                return param["contents"]
            case "AbiBytes" | "AbiBytesDynamic":
                is_fixed_size = isinstance(param["contents"], list)
                contents = param["contents"][1] if is_fixed_size else param["contents"]

                # Haskell encoding needs to be stripped and then converted to a hex literal
                return parse_echidna_byte_string(contents.strip('"'))
            case "AbiString":
                # TODO Strings are not converted correctly, they're pure hex for now
                hex_string = parse_echidna_byte_string(param["contents"].strip('"'))
                return bytes.fromhex(hex_string).decode("utf-8")
            case _:
                handle_exit(
                    f"\n* The parameter tag `{param['tag']}` could not be found in the call object. This could indicate an issue in decoding the call sequence, or a missing feature. Please open an issue at https://github.com/crytic/fuzz-utils/issues"
                )

    def _match_array_type(
        self, param: dict, index: int, input_parameter: Any
    ) -> tuple[list, int] | NoReturn:
        match param["tag"]:
            case "AbiArray":
                # Consider cases where the array items are more complex types (bytes, string, tuples)
                func_params = self._decode_function_params(
                    param["contents"][2], True, input_parameter
                )
                return func_params, index
            case "AbiArrayDynamic":
                # Consider cases where the array items are more complex types (bytes, string, tuples)
                func_params = self._decode_function_params(
                    param["contents"][1], True, input_parameter
                )
                index += 1

                return func_params, index
            case _:
                handle_exit(
                    f"\n* The parameter tag `{param['tag']}` could not be found in the call object. This could indicate an issue in decoding the call sequence, or a missing feature. Please open an issue at https://github.com/crytic/fuzz-utils/issues"
                )

    def _match_user_defined_type(self, param: dict, input_parameter: Any) -> str | NoReturn:
        match param["tag"]:
            case "AbiTuple":
                match input_parameter.type:
                    case Structure() | StructureContract():  # type: ignore[misc]
                        entry_point = input_parameter.type.elems_ordered  # type: ignore[unreachable]
                        func_params = self._decode_function_params(  # type: ignore[unreachable]
                            param["contents"], True, entry_point
                        )
                        struct_params = {}
                        for param_idx, parameter in enumerate(func_params):
                            field_parameter = entry_point[param_idx].name
                            struct_params[f"{field_parameter}"] = parameter

                        return struct_params
                    case _:
                        handle_exit(
                            f"\n* The parameter type `{input_parameter.type}` could not be found. This could indicate an issue in decoding the call sequence, or a missing feature. Please open an issue at https://github.com/crytic/fuzz-utils/issues"
                        )
            case "AbiUInt":
                if isinstance(input_parameter.type, Enum):
                    enum_uint = self._match_elementary_types(param)
                    return enum_uint

                # TODO is this even reachable?
                handle_exit(
                    f"\n* The parameter type `{input_parameter.type}` does not match the intended type `Enum`. This could indicate an issue in decoding the call sequence, or a missing feature. Please open an issue at https://github.com/crytic/fuzz-utils/issues"
                )
            case _:
                handle_exit(
                    f"\n* The parameter tag `{param['tag']}` could not be found in the call object. This could indicate an issue in decoding the call sequence, or a missing feature. Please open an issue at https://github.com/crytic/fuzz-utils/issues"
                )

    # Load the corpus and reproducers one by one
    def _fetch_corpus(self) -> tuple[list, list, list, list]:
        """Fetches the Echidna coverage and reproducers from the corpus and returns two lists"""
        coverage_list: list = []
        reproducers_list: list = []

        coverage_path = os.path.join(self.corpus_path, "coverage")
        reproducers_path = os.path.join(self.corpus_path, "reproducers")

        coverage_file_names, coverage_list = self._parse_files(coverage_path)
        reproducers_file_names, reproducers_list = self._parse_files(reproducers_path)

        return coverage_list, reproducers_list, coverage_file_names, reproducers_file_names

    def _parse_files(self, path: str) -> tuple[list, list]:
        """Parses all files in a directory and returns a list"""
        name_list = []
        file_list = []
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)

            if os.path.isfile(full_path):
                with open(full_path, "r", encoding="utf8") as file:
                    file_list.append(json.load(file))
                    name_list.append(entry.split(".")[0])

        return name_list, file_list  ##
