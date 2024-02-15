""" Generates a test file from Echidna reproducers """
import os
import sys
import json
import argparse
import jinja2

from pkg_resources import require

from slither import Slither
from slither.core.declarations.contract import Contract
from fuzz_utils.utils.crytic_print import CryticPrint
from fuzz_utils.templates.foundry_templates import templates
from fuzz_utils.fuzzers.Medusa import Medusa
from fuzz_utils.fuzzers.Echidna import Echidna
from fuzz_utils.utils.error_handler import handle_exit


class FoundryTest:
    """
    Handles the generation of Foundry test files
    """

    def __init__(
        self,
        inheritance_path: str,
        target_name: str,
        corpus_path: str,
        test_dir: str,
        slither: Slither,
        fuzzer: Echidna | Medusa,
    ) -> None:
        self.inheritance_path = inheritance_path
        self.target_name = target_name
        self.corpus_path = corpus_path
        self.test_dir = test_dir
        self.slither = slither
        self.target = self.get_target_contract()
        self.fuzzer = fuzzer

    def get_target_contract(self) -> Contract:
        """Gets the Slither Contract object for the specified contract file"""
        contracts = self.slither.get_contract_from_name(self.target_name)
        # Loop in case slither fetches multiple contracts for some reason (e.g., similar names?)
        for contract in contracts:
            if contract.name == self.target_name:
                return contract

        # TODO throw error if no contract found
        sys.exit(-1)

    def create_poc(self) -> str:
        """Takes in a directory path to the echidna reproducers and generates a test file"""

        file_list = []
        tests_list = []
        # 1. Iterate over each reproducer file (open it)
        for entry in os.listdir(self.fuzzer.reproducer_dir):
            full_path = os.path.join(self.fuzzer.reproducer_dir, entry)

            if os.path.isfile(full_path):
                try:
                    with open(full_path, "r", encoding="utf-8") as file:
                        file_list.append(json.load(file))
                except Exception:  # pylint: disable=broad-except
                    print(f"Fail on {full_path}")

        # 2. Parse each reproducer file and add each test function to the functions list
        for idx, file in enumerate(file_list):
            try:
                tests_list.append(self.fuzzer.parse_reproducer(file, idx))
            except Exception:  # pylint: disable=broad-except
                print(f"Parsing fail on {file}: index: {idx}")

        # 4. Generate the test file
        template = jinja2.Template(templates["CONTRACT"])
        write_path = f"{self.test_dir}{self.target_name}"
        inheritance_path = f"{self.inheritance_path}{self.target_name}"

        # 5. Save the test file
        test_file_str = template.render(
            file_path=f"{inheritance_path}.sol",
            target_name=self.target_name,
            amount=0,
            tests=tests_list,
            fuzzer=self.fuzzer.name,
        )
        with open(f"{write_path}_{self.fuzzer.name}_Test.t.sol", "w", encoding="utf-8") as outfile:
            outfile.write(test_file_str)
        CryticPrint().print_success(
            f"Generated a test file in {write_path}_{self.fuzzer.name}_Test.t.sol"
        )

        return test_file_str


def main() -> None:  # type: ignore[func-returns-value]
    """The main entry point"""
    parser = argparse.ArgumentParser(
        prog="fuzz-utils", description="Generate test harnesses for Echidna failed properties."
    )
    parser.add_argument("file_path", help="Path to the Echidna test harness.")
    parser.add_argument(
        "-cd", "--corpus-dir", dest="corpus_dir", help="Path to the corpus directory", required=True
    )
    parser.add_argument("-c", "--contract", dest="target_contract", help="Define the contract name")
    parser.add_argument(
        "-td",
        "--test-directory",
        dest="test_directory",
        help="Define the directory that contains the Foundry tests.",
    )
    parser.add_argument(
        "-i",
        "--inheritance-path",
        dest="inheritance_path",
        help="Define the relative path from the test directory to the directory src/contracts directory.",
    )
    parser.add_argument(
        "-f",
        "--fuzzer",
        dest="selected_fuzzer",
        help="Define the fuzzer used. Valid inputs: 'echidna', 'medusa'",
    )
    parser.add_argument(
        "--version",
        help="displays the current version",
        version=require("fuzz-utils")[0].version,
        action="version",
    )

    args = parser.parse_args()

    missing_args = [arg for arg, value in vars(args).items() if value is None]
    if missing_args:
        parser.print_help()
        handle_exit(f"\n* Missing required arguments: {', '.join(missing_args)}")

    file_path = args.file_path
    corpus_dir = args.corpus_dir
    test_directory = args.test_directory
    inheritance_path = args.inheritance_path
    target_contract = args.target_contract
    slither = Slither(file_path)
    fuzzer: Echidna | Medusa

    match args.selected_fuzzer.lower():
        case "echidna":
            fuzzer = Echidna(target_contract, corpus_dir, slither)
        case "medusa":
            fuzzer = Medusa(target_contract, corpus_dir, slither)
        case _:
            handle_exit(
                f"\n* The requested fuzzer {args.selected_fuzzer} is not supported. Supported fuzzers: echidna, medusa."
            )

    CryticPrint().print_information(
        f"Generating Foundry unit tests based on the {fuzzer.name} reproducers..."
    )
    foundry_test = FoundryTest(
        inheritance_path, target_contract, corpus_dir, test_directory, slither, fuzzer
    )
    foundry_test.create_poc()
    CryticPrint().print_success("Done!")


if __name__ == "__main__":
    sys.exit(main())  # type: ignore[func-returns-value]
