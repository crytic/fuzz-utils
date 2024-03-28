""" Globally available fixtures"""
import os
import subprocess
import re
from typing import Any, Callable
import pytest

from slither import Slither
from fuzz_utils.generate.FoundryTest import FoundryTest
from fuzz_utils.generate.fuzzers.Echidna import Echidna
from fuzz_utils.generate.fuzzers.Medusa import Medusa


class TestGenerator:
    """Helper class for testing all fuzzers with the tool"""

    __test__ = False

    def __init__(self, target: str, target_path: str, corpus_dir: str):
        slither = Slither(target_path)
        echidna = Echidna(target, f"echidna-corpora/{corpus_dir}", slither, False)
        medusa = Medusa(target, f"medusa-corpora/{corpus_dir}", slither, False)
        config = {
            "targetContract": target,
            "inheritancePath": "../src/",
            "corpusDir": f"echidna-corpora/{corpus_dir}",
            "testsDir": "./test/",
            "allSequences": False,
        }
        self.echidna_generator = FoundryTest(config, slither, echidna)
        config["corpusDir"] = f"medusa-corpora/{corpus_dir}"
        self.medusa_generator = FoundryTest(config, slither, medusa)

    def echidna_generate_tests(self) -> None:
        """Runs the fuzz-utils tool for an Echidna corpus"""
        self.echidna_generator.create_poc()

    def medusa_generate_tests(self) -> None:
        """Runs the fuzz-utils tool for a Medusa corpus"""
        self.medusa_generator.create_poc()


@pytest.fixture(autouse=True)  # type: ignore[misc]
def change_test_dir(request: Any, monkeypatch: Any) -> None:
    """Helper fixture to change the working directory"""
    # Directory of the test file
    test_dir = request.fspath.dirname

    # Path to the test_data directory
    data_dir = os.path.join(test_dir, "test_data")

    # Change the current working directory to test_data
    monkeypatch.chdir(data_dir)


@pytest.fixture  # type: ignore[misc]
def basic_types() -> TestGenerator:
    """Fixture for the BasicTypes test contract"""
    target = "BasicTypes"
    target_path = "./src/BasicTypes.sol"
    corpus_dir = "corpus-basic"

    return TestGenerator(target, target_path, corpus_dir)


@pytest.fixture  # type: ignore[misc]
def fixed_size_arrays() -> TestGenerator:
    """Fixture for the FixedArrays test contract"""
    target = "FixedArrays"
    target_path = "./src/FixedArrays.sol"
    corpus_dir = "corpus-fixed-arr"

    return TestGenerator(target, target_path, corpus_dir)


@pytest.fixture  # type: ignore[misc]
def dynamic_arrays() -> TestGenerator:
    """Fixture for the DynamicArrays test contract"""
    target = "DynamicArrays"
    target_path = "./src/DynamicArrays.sol"
    corpus_dir = "corpus-dyn-arr"

    return TestGenerator(target, target_path, corpus_dir)


@pytest.fixture  # type: ignore[misc]
def structs_and_enums() -> TestGenerator:
    """Fixture for the TupleTypes test contract"""
    target = "TupleTypes"
    target_path = "./src/TupleTypes.sol"
    corpus_dir = "corpus-struct"

    return TestGenerator(target, target_path, corpus_dir)


@pytest.fixture  # type: ignore[misc]
def value_transfer() -> TestGenerator:
    """Fixture for the ValueTransfer test contract"""
    target = "ValueTransfer"
    target_path = "./src/ValueTransfer.sol"
    corpus_dir = "corpus-value"

    return TestGenerator(target, target_path, corpus_dir)


def run_generation_command_test(
    generate_tests: Callable, test_name: str, fuzzer: str, pattern: str
) -> None:
    """Utility function to test unit test generation from a corpus and contract"""
    generate_tests()
    # Ensure the file was created
    path = os.path.join(os.getcwd(), "test", f"{test_name}_{fuzzer}_Test.t.sol")
    assert os.path.exists(path)

    # Ensure the file can be compiled
    subprocess.run(["forge", "build", "--build-info"], capture_output=True, text=True, check=True)

    # Ensure the file can be tested
    result = subprocess.run(
        ["forge", "test", "--match-contract", f"{test_name}_{fuzzer}_Test"],
        capture_output=True,
        text=True,
        check=False,
    )

    # Remove ansi escape sequences
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    output = ansi_escape.sub("", result.stdout)

    # Ensure all tests fail
    match = re.search(pattern, output)
    if match:
        tests_passed = int(match.group(2))
        assert tests_passed == 0
    else:
        assert False, "No tests were ran"
