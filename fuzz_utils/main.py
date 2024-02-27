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
from fuzz_utils.converters.EchidnaConverter import EchidnaConverter
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

    def create_poc(self, no_save: bool) -> str:
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
        if not no_save:
            test_file_str = template.render(
                file_path=f"{inheritance_path}.sol",
                target_name=self.target_name,
                amount=0,
                tests=tests_list,
                fuzzer=self.fuzzer.name,
            )
            with open(
                f"{write_path}_{self.fuzzer.name}_Test.t.sol", "w", encoding="utf-8"
            ) as outfile:
                outfile.write(test_file_str)
            CryticPrint().print_success(
                f"Generated a test file in {write_path}_{self.fuzzer.name}_Test.t.sol"
            )
            return test_file_str

        CryticPrint().print_success(
            "No files were saved. File saving is turned off using the --no-save flag"
        )

        return ""


# pylint: disable=too-many-locals,too-many-branches,too-many-statements
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
    parser_generate.add_argument(
        "--no-save",
        dest="no_save",
        action="store_true",
    )

    # The command parser for converting between corpus formats
    parser_convert = subparsers.add_parser(
        "convert", help="Convert a Echidna/Medusa corpus into the other format."
    )
    parser_convert.add_argument("file_path", help="Path to the Echidna/Medusa test harness.")
    parser_convert.add_argument(
        "-cd", "--corpus-dir", dest="corpus_dir", help="Path to the corpus directory", required=True
    )
    parser_convert.add_argument(
        "-c", "--contract", dest="target_contract", required=True, help="Define the contract name"
    )
    parser_convert.add_argument(
        "-f",
        "--fuzzer",
        dest="selected_fuzzer",
        required=True,
        help="Define the fuzzer used. Valid inputs: 'echidna', 'medusa'",
    )
    parser_convert.add_argument(
        "-gfc",
        "--gas-fee-cap",
        dest="gas_fee_cap",
        help="Define the gasFeeCap to be used in Medusa corpora.",
    )
    parser_convert.add_argument(
        "-gtc",
        "--gas-tip-cap",
        dest="gas_tip_cap",
        help="Define the gasTipCap to be used in Medusa corpora.",
    )
    parser_convert.add_argument(
        "-o",
        "--output-dir",
        dest="output_dir",
        help="Define the output directory where the result will be saved.",
    )
    parser_convert.add_argument(
        "-t",
        "--target-address",
        dest="target_address",
        help="Define the address of the target contract. Needed because Medusa and Echidna deploy contracts to different addresses",
    )
    parser_convert.add_argument(
        "-d",
        "--deployer",
        dest="deployer",
        help="Define the address of the Echidna/Medusa deployer.",
    )

    args = parser.parse_args()
    selected_fuzzer = args.selected_fuzzer.lower()
    file_path = args.file_path
    corpus_dir = args.corpus_dir
    target_contract = args.target_contract
    slither = Slither(file_path)

    if args.command == "generate":
        test_directory = args.test_directory
        inheritance_path = args.inheritance_path

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
        foundry_test.create_poc(no_save=args.no_save)
        CryticPrint().print_success("Done!")
    elif args.command == "convert":
        corpus_dir = args.corpus_dir
        output_dir = args.output_dir
        match selected_fuzzer:
            case "echidna":
                CryticPrint().print_information(
                    f"Converting Echidna corpus {corpus_dir} to Medusa format..."
                )
                converter = EchidnaConverter(
                    target_contract,
                    corpus_dir,
                    args.gas_fee_cap,
                    args.gas_tip_cap,
                    slither,
                    args.target_address,
                    args.deployer,
                )
                (
                    converted_coverage,
                    converted_reproducers,
                    coverage_file_names,
                    reproducers_file_names,
                ) = converter.convert()

                # TODO Check if output dir exists
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                    CryticPrint().print_success(f"{output_dir} created!")

                if not os.path.exists(output_dir + "/call_sequences"):
                    os.makedirs(output_dir + "/call_sequences/immutable")
                    os.makedirs(output_dir + "/call_sequences/mutable")

                if not os.path.exists(output_dir + "/test_results"):
                    os.makedirs(output_dir + "/test_results")

                # Check if "coverage" and "reproducers" dirs exist

                for idx, file_name in enumerate(coverage_file_names):
                    coverage_file = "[" + ",".join(converted_coverage[idx]) + "]"
                    with open(
                        f"{output_dir}/call_sequences/mutable/{file_name}.json",
                        "w",
                        encoding="utf-8",
                    ) as outfile:
                        outfile.write(coverage_file)
                    with open(
                        f"{output_dir}/call_sequences/immutable/{file_name}.json",
                        "w",
                        encoding="utf-8",
                    ) as outfile:
                        outfile.write(coverage_file)

                for idx, file_name in enumerate(reproducers_file_names):
                    reproducer_file = "[" + ",".join(converted_reproducers[idx]) + "]"
                    with open(
                        f"{output_dir}/test_results/{file_name}.json", "w", encoding="utf-8"
                    ) as outfile:
                        outfile.write(reproducer_file)

                CryticPrint().print_success(f"Medusa corpus was saved to {output_dir}!")
            case _:
                pass
    else:
        parser.print_help()


if __name__ == "__main__":
    sys.exit(main())  # type: ignore[func-returns-value]
