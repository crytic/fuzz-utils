""" Tests for generating compilable test files from an Medusa corpus"""
from pathlib import Path
import os
import re
import subprocess
import pytest
from .conftest import TestGenerator

TEST_DATA_DIR = Path(__file__).resolve().parent / "test_data"
PATTERN = r"(\d+)\s+failing tests,\s+(\d+)\s+tests succeeded"


def test_medusa_basic_types(basic_types: TestGenerator) -> None:
    """Tests the BasicTypes contract with a Medusa corpus"""
    basic_types.medusa_generate_tests()
    # Ensure the file was created
    path = os.path.join(os.getcwd(), "test", "BasicTypes_Medusa_Test.t.sol")
    assert os.path.exists(path)

    # Ensure the file can be compiled
    subprocess.run(["forge", "build", "--build-info"], capture_output=True, text=True, check=True)

    # Ensure the file can be tested
    result = subprocess.run(
        ["forge", "test", "--match-contract", "BasicTypes_Medusa_Test"],
        capture_output=True,
        text=True,
        check=False,
    )

    # Remove ansi escape sequences
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    output = ansi_escape.sub("", result.stdout)

    # Ensure all tests fail
    match = re.search(PATTERN, output)
    if match:
        tests_passed = int(match.group(2))
        assert tests_passed == 0
    else:
        assert False, "No tests were ran"


def test_medusa_fixed_array_types(fixed_size_arrays: TestGenerator) -> None:
    """Tests the FixedArrays contract with a Medusa corpus"""
    fixed_size_arrays.medusa_generate_tests()
    # Ensure the file was created
    path = os.path.join(os.getcwd(), "test", "FixedArrays_Medusa_Test.t.sol")
    assert os.path.exists(path)

    # Ensure the file can be compiled
    subprocess.run(["forge", "build", "--build-info"], capture_output=True, text=True, check=True)

    # Ensure the file can be tested
    result = subprocess.run(
        ["forge", "test", "--match-contract", "FixedArrays_Medusa_Test"],
        capture_output=True,
        text=True,
        check=False,
    )

    # Remove ansi escape sequences
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    output = ansi_escape.sub("", result.stdout)

    # Ensure all tests fail
    match = re.search(PATTERN, output)
    if match:
        tests_passed = int(match.group(2))
        assert tests_passed == 0
    else:
        assert False, "No tests were ran"


def test_medusa_dynamic_array_types(dynamic_arrays: TestGenerator) -> None:
    """Tests the DynamicArrays contract with a Medusa corpus"""
    dynamic_arrays.medusa_generate_tests()
    # Ensure the file was created
    path = os.path.join(os.getcwd(), "test", "DynamicArrays_Medusa_Test.t.sol")
    assert os.path.exists(path)

    # Ensure the file can be compiled
    subprocess.run(["forge", "build", "--build-info"], capture_output=True, text=True, check=True)

    # Ensure the file can be tested
    result = subprocess.run(
        ["forge", "test", "--match-contract", "DynamicArrays_Medusa_Test"],
        capture_output=True,
        text=True,
        check=False,
    )

    # Remove ansi escape sequences
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    output = ansi_escape.sub("", result.stdout)

    # Ensure all tests fail
    match = re.search(PATTERN, output)
    if match:
        tests_passed = int(match.group(2))
        assert tests_passed == 0
    else:
        assert False, "No tests were ran"


def test_medusa_structs_and_enums(structs_and_enums: TestGenerator) -> None:
    """Tests the TupleTypes contract with a Medusa corpus"""
    structs_and_enums.medusa_generate_tests()
    # Ensure the file was created
    path = os.path.join(os.getcwd(), "test", "TupleTypes_Medusa_Test.t.sol")
    assert os.path.exists(path)

    # Ensure the file can be compiled
    subprocess.run(["forge", "build", "--build-info"], capture_output=True, text=True, check=True)

    # Ensure the file can be tested
    result = subprocess.run(
        ["forge", "test", "--match-contract", "TupleTypes_Medusa_Test"],
        capture_output=True,
        text=True,
        check=False,
    )

    # Remove ansi escape sequences
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    output = ansi_escape.sub("", result.stdout)

    # Ensure all tests fail
    match = re.search(PATTERN, output)
    if match:
        tests_passed = int(match.group(2))
        assert tests_passed == 0
    else:
        assert False, "No tests were ran"


@pytest.mark.xfail(strict=True)  # type: ignore[misc]
def test_medusa_value_transfer(value_transfer: TestGenerator) -> None:
    """Tests the BasicTypes contract with a Medusa corpus"""
    value_transfer.medusa_generate_tests()
    # Ensure the file was created
    path = os.path.join(os.getcwd(), "test", "ValueTransfer_Medusa_Test.t.sol")
    assert os.path.exists(path)

    # Ensure the file can be compiled
    subprocess.run(["forge", "build", "--build-info"], capture_output=True, text=True, check=True)

    # Ensure the file can be tested
    result = subprocess.run(
        ["forge", "test", "--match-contract", "ValueTransfer_Medusa_Test"],
        capture_output=True,
        text=True,
        check=False,
    )

    # Remove ansi escape sequences
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    output = ansi_escape.sub("", result.stdout)

    # Ensure all tests fail
    match = re.search(PATTERN, output)
    if match:
        tests_passed = int(match.group(2))
        assert tests_passed == 0
    else:
        assert False, "No tests were ran"
