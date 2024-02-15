""" Globally available fixtures"""
import os
from typing import Any
import pytest

from slither import Slither
from fuzz_utils.main import FoundryTest
from fuzz_utils.fuzzers.Echidna import Echidna
from fuzz_utils.fuzzers.Medusa import Medusa


class TestGenerator:
    """Helper class for testing all fuzzers with the tool"""

    def __init__(self, target: str, target_path: str, corpus_dir: str):
        slither = Slither(target_path)
        echidna = Echidna(target, f"echidna-corpora/{corpus_dir}", slither)
        medusa = Medusa(target, f"medusa-corpora/{corpus_dir}", slither)
        self.echidna_generator = FoundryTest(
            "../src/", target, f"echidna-corpora/{corpus_dir}", "./test/", slither, echidna
        )
        self.medusa_generator = FoundryTest(
            "../src/", target, f"medusa-corpora/{corpus_dir}", "./test/", slither, medusa
        )

    def echidna_generate_tests(self) -> None:
        """Runs the test-generator tool for an Echidna corpus"""
        self.echidna_generator.create_poc()

    def medusa_generate_tests(self) -> None:
        """Runs the test-generator tool for a Medusa corpus"""
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
