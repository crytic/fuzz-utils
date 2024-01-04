""" Generates a test file from Echidna reproducers """
import os
import sys
import json
import argparse
import jinja2

from slither import Slither
from slither.core.declarations.contract import Contract
from test_generator.utils.crytic_print import CryticPrint
from test_generator.templates.foundry_templates import templates
from test_generator.fuzzers.Medusa import Medusa
from test_generator.fuzzers.Echidna import Echidna


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
        self.target = self._get_target_contract()
        self.fuzzer = fuzzer

    def _get_target_contract(self) -> Contract:
        contracts = self.slither.get_contract_from_name(self.target_name)
        # Loop in case slither fetches multiple contracts for some reason (e.g., similar names?)
        for contract in contracts:
            if contract.name == self.target_name:
                return contract

        # TODO throw error if no contract found
        exit(-1)

    def create_poc(self) -> str:
        """Takes in a directory path to the echidna reproducers and generates a test file"""

        file_list = []
        tests_list = []
        # 1. Iterate over each reproducer file (open it)
        for entry in os.listdir(self.fuzzer.reproducer_dir):
            full_path = os.path.join(self.fuzzer.reproducer_dir, entry)

            if os.path.isfile(full_path):
                with open(full_path, "r", encoding="utf8") as file:
                    file_list.append(json.load(file))

        # 2. Parse each reproducer file and add each test function to the functions list
        for idx, file in enumerate(file_list):
            tests_list.append(self.fuzzer.parse_reproducer(file, idx))

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


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="test-generator", description="Generate test harnesses for Echidna failed properties."
    )
    parser.add_argument("file_path", help="Path to the Echidna test harness.")
    parser.add_argument(
        "-cd", "--corpus-dir", dest="corpus_dir", help="Path to the corpus directory"
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

    args = parser.parse_args()
    file_path = args.file_path
    corpus_dir = args.corpus_dir
    test_directory = args.test_directory
    inheritance_path = args.inheritance_path
    target_contract = args.target_contract
    slither = Slither(file_path)
    fuzzer = None

    match args.selected_fuzzer.lower():
        case "echidna":
            fuzzer = Echidna(target_contract, corpus_dir, slither)
        case "medusa":
            fuzzer = Medusa(target_contract, corpus_dir, slither)
        case _:
            # TODO create a descriptive error
            exit(-1)

    CryticPrint().print_information(
        f"Generating Foundry unit tests based on the {fuzzer.name} reproducers..."
    )
    test_generator = FoundryTest(
        inheritance_path, target_contract, corpus_dir, test_directory, slither, fuzzer
    )
    test_generator.create_poc()
    CryticPrint().print_success("Done!")


if __name__ == "__main__":
    sys.exit(main())
