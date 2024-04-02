"""The FoundryTest class that handles generation of unit tests from call sequences"""
import os
import json
import copy
from typing import Any
import jinja2

from slither import Slither
from fuzz_utils.utils.crytic_print import CryticPrint
from fuzz_utils.utils.slither_utils import get_target_contract
from fuzz_utils.templates.default_config import default_config

from fuzz_utils.generate.fuzzers.Medusa import Medusa
from fuzz_utils.generate.fuzzers.Echidna import Echidna
from fuzz_utils.templates.foundry_templates import templates

# pylint: disable=too-few-public-methods,too-many-instance-attributes
class FoundryTest:
    """
    Handles the generation of Foundry test files
    """

    config: dict = copy.deepcopy(default_config["generate"])

    def __init__(
        self,
        config: dict,
        slither: Slither,
        fuzzer: Echidna | Medusa,
    ) -> None:
        self.slither = slither
        for key, value in config.items():
            if key in self.config:
                self.config[key] = value

        self.target = get_target_contract(self.slither, self.config["targetContract"])
        self.target_file_name = self.target.source_mapping.filename.relative.split("/")[-1]
        self.fuzzer = fuzzer

    def create_poc(self) -> str:
        """Takes in a directory path to the echidna reproducers and generates a test file"""

        file_list: list[dict[str, Any]] = []
        tests_list = []
        dir_list = []
        if self.config["allSequences"]:
            dir_list = self.fuzzer.corpus_dirs
        else:
            dir_list = [self.fuzzer.reproducer_dir]

        # 1. Iterate over each directory and reproducer file (open it)
        for directory in dir_list:
            for entry in os.listdir(directory):
                full_path = os.path.join(directory, entry)

                if os.path.isfile(full_path):
                    try:
                        with open(full_path, "r", encoding="utf-8") as file:
                            file_list.append({"path": full_path, "content": json.load(file)})
                    except Exception:  # pylint: disable=broad-except
                        print(f"Fail on {full_path}")

        # 2. Parse each reproducer file and add each test function to the functions list
        for idx, file_obj in enumerate(file_list):
            try:
                tests_list.append(
                    self.fuzzer.parse_reproducer(file_obj["path"], file_obj["content"], idx)
                )
            except Exception:  # pylint: disable=broad-except
                print(f"Parsing fail on {file_obj['content']}: index: {idx}")

        # 4. Generate the test file
        template = jinja2.Template(templates["CONTRACT"])
        write_path = os.path.join(self.config["testsDir"], self.config["targetContract"])
        inheritance_path = os.path.join(self.config["inheritancePath"])
        # 5. Save the test file
        test_file_str = template.render(
            file_path=inheritance_path,
            target_name=self.config["targetContract"],
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
