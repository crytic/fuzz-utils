"""The FoundryTest class that handles generation of unit tests from call sequences"""
import os
import sys
import json
import jinja2

from slither import Slither
from slither.core.declarations.contract import Contract
from fuzz_utils.utils.crytic_print import CryticPrint

from fuzz_utils.generate.fuzzers.Medusa import Medusa
from fuzz_utils.generate.fuzzers.Echidna import Echidna
from fuzz_utils.templates.foundry_templates import templates


class FoundryTest:
    """
    Handles the generation of Foundry test files
    """

    def __init__(
        self,
        config: dict,
        slither: Slither,
        fuzzer: Echidna | Medusa,
    ) -> None:
        self.inheritance_path = config["inheritancePath"]
        self.target_name = config["targetContract"]
        self.corpus_path = config["corpusDir"]
        self.test_dir = config["testsDir"]
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
