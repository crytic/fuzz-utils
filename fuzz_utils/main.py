""" Generates a test file from Echidna reproducers """
import os
import sys
import json
import argparse
import subprocess
import re
import jinja2

from pkg_resources import require

from slither import Slither
from slither.core.declarations.contract import Contract
from fuzz_utils.utils.crytic_print import CryticPrint
from fuzz_utils.templates.foundry_templates import templates
from fuzz_utils.fuzzers.Medusa import Medusa
from fuzz_utils.fuzzers.Echidna import Echidna
from fuzz_utils.templates.HarnessGenerator import HarnessGenerator
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


def find_remappings(include_attacks: bool) -> dict:
    """Finds the remappings used and returns a dict with the values"""
    CryticPrint().print_information("Checking dependencies...")
    openzeppelin = r"(\S+)=lib\/openzeppelin-contracts\/(?!\S*lib\/)(\S+)"
    solmate = r"(\S+)=lib\/solmate\/(?!\S*lib\/)(\S+)"
    properties = r"(\S+)=lib\/properties\/(?!\S*lib\/)(\S+)"
    remappings: str = ""

    if os.path.exists("remappings.txt"):
        with open("remappings.txt", "r", encoding="utf-8") as file:
            remappings = file.read()
    else:
        output = subprocess.run(["forge", "remappings"], capture_output=True, text=True, check=True)
        remappings = str(output)

    oz_matches = re.findall(openzeppelin, remappings)
    sol_matches = re.findall(solmate, remappings)
    prop_matches = re.findall(properties, remappings)

    if include_attacks and len(oz_matches) == 0 and len(sol_matches) == 0:
        handle_exit(
            "Please make sure that openzeppelin-contracts or solmate are installed if you're using the Attack templates."
        )

    if len(prop_matches) == 0:
        handle_exit(
            "Please make sure crytic/properties is installed before running the template command."
        )

    result = {}
    if len(oz_matches) > 0:
        default = ["contracts/"]
        result["openzeppelin"] = "".join(
            find_difference_between_list_and_tuple(default, oz_matches[0])
        )

    if len(sol_matches) > 0:
        default = ["src/"]
        result["solmate"] = "".join(find_difference_between_list_and_tuple(default, sol_matches[0]))

    if len(prop_matches) > 0:
        default = ["contracts/"]
        result["properties"] = "".join(
            find_difference_between_list_and_tuple(default, prop_matches[0])
        )

    return result


def find_difference_between_list_and_tuple(default: list, my_tuple: tuple) -> list:
    """Used to manage remapping paths based on difference between the remappings and the expected path"""
    return [item for item in my_tuple if item not in default] + [
        item for item in default if item not in my_tuple
    ]


# pylint: disable=too-many-locals
def main() -> None:  # type: ignore[func-returns-value]
    """The main entry point"""
    parser = argparse.ArgumentParser(
        prog="fuzz-utils", description="Generate test harnesses for Echidna failed properties."
    )
    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    # The command parser for generating unit tests
    parser_generate = subparsers.add_parser(
        "generate", help="Generate unit tests from fuzzer corpora sequences."
    )
    parser_generate.add_argument("file_path", help="Path to the Echidna/Medusa test harness.")
    parser_generate.add_argument(
        "-cd", "--corpus-dir", dest="corpus_dir", help="Path to the corpus directory", required=True
    )
    parser_generate.add_argument(
        "-c", "--contract", dest="target_contract", help="Define the contract name"
    )
    parser_generate.add_argument(
        "-td",
        "--test-directory",
        dest="test_directory",
        help="Define the directory that contains the Foundry tests.",
    )
    parser_generate.add_argument(
        "-i",
        "--inheritance-path",
        dest="inheritance_path",
        help="Define the relative path from the test directory to the directory src/contracts directory.",
    )
    parser_generate.add_argument(
        "-f",
        "--fuzzer",
        dest="selected_fuzzer",
        help="Define the fuzzer used. Valid inputs: 'echidna', 'medusa'",
    )
    parser_generate.add_argument(
        "--version",
        help="displays the current version",
        version=require("fuzz-utils")[0].version,
        action="version",
    )

    # The command parser for converting between corpus formats
    parser_template = subparsers.add_parser(
        "template", help="Generate a templated fuzzing harness."
    )
    parser_template.add_argument("file_path", help="Path to the Solidity contract.")
    parser_template.add_argument(
        "-c",
        "--contracts",
        dest="target_contracts",
        nargs="+",
        help="Define a list of target contracts for the harness.",
    )
    parser_template.add_argument(
        "-o",
        "--output-dir",
        dest="output_dir",
        help="Define the output directory where the result will be saved.",
    )
    parser_template.add_argument(
        "--config", dest="config", help="Define the location of the config file."
    )
    args = parser.parse_args()
    file_path = args.file_path
    CryticPrint().print_information("Running Slither...")
    slither = Slither(file_path)

    if args.command == "generate":
        test_directory = args.test_directory
        inheritance_path = args.inheritance_path
        selected_fuzzer = args.selected_fuzzer.lower()
        corpus_dir = args.corpus_dir
        target_contract = args.target_contract

        fuzzer: Echidna | Medusa

        match selected_fuzzer:
            case "echidna":
                fuzzer = Echidna(target_contract, corpus_dir, slither)
            case "medusa":
                fuzzer = Medusa(target_contract, corpus_dir, slither)
            case _:
                handle_exit(
                    f"\n* The requested fuzzer {selected_fuzzer} is not supported. Supported fuzzers: echidna, medusa."
                )

        CryticPrint().print_information(
            f"Generating Foundry unit tests based on the {fuzzer.name} reproducers..."
        )
        foundry_test = FoundryTest(
            inheritance_path, target_contract, corpus_dir, test_directory, slither, fuzzer
        )
        foundry_test.create_poc()
        CryticPrint().print_success("Done!")
    elif args.command == "template":
        config: dict = {}
        if args.output_dir:
            output_dir = os.path.join("./test", args.output_dir)
        else:
            output_dir = os.path.join("./test", "fuzzing")
        if args.config:
            with open(args.config, "r", encoding="utf-8") as readFile:
                config = json.load(readFile)

        # Check if dependencies are installed
        include_attacks = bool("attacks" in config and len(config["attacks"]) > 0)
        remappings = find_remappings(include_attacks)

        generator = HarnessGenerator(
            file_path, args.target_contracts, slither, output_dir, config, remappings
        )
        generator.generate_templates()
    else:
        parser.print_help()


if __name__ == "__main__":
    sys.exit(main())  # type: ignore[func-returns-value]
