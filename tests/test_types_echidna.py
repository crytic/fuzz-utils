""" BasicTypes tests"""
from pathlib import Path
import os
import re
import subprocess

TEST_DATA_DIR = Path(__file__).resolve().parent / "test_data"
PATTERN = r"(\d+)\s+failing tests,\s+(\d+)\s+tests succeeded"

def test_echidna_basic_types(basic_types):
    basic_types.echidna_generate_tests()
    # Ensure the file was created
    path = os.path.join(os.getcwd(), "test", "BasicTypes_Echidna_Test.t.sol")
    assert os.path.exists(path)

    # Ensure the file can be compiled and tested
    result = subprocess.run(["forge", "test", "--match-contract", "BasicTypes_Echidna_Test"], capture_output=True, text=True, check=False)
    output = result.stdout

    # Remove ansi escape sequences
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    result = ansi_escape.sub('', output)

    # Ensure all tests fail
    match = re.search(PATTERN, result)
    if match:
        tests_passed = int(match.group(2))
        assert tests_passed == 0
    else:
        assert False, "No tests were ran"

def test_echidna_fixed_array_types(fixed_size_arrays):
    fixed_size_arrays.echidna_generate_tests()
    # Ensure the file was created
    path = os.path.join(os.getcwd(), "test", "FixedArrays_Echidna_Test.t.sol")
    assert os.path.exists(path)

    # Ensure the file can be compiled and tested
    result = subprocess.run(["forge", "test", "--match-contract", "FixedArrays_Echidna_Test"], capture_output=True, text=True, check=False)
    output = result.stdout

    # Remove ansi escape sequences
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    result = ansi_escape.sub('', output)

    # Ensure all tests fail
    match = re.search(PATTERN, result)
    if match:
        tests_passed = int(match.group(2))
        assert tests_passed == 0
    else:
        assert False, "No tests were ran"

def test_echidna_dynamic_array_types(dynamic_arrays):
    dynamic_arrays.echidna_generate_tests()
    # Ensure the file was created
    path = os.path.join(os.getcwd(), "test", "DynamicArrays_Echidna_Test.t.sol")
    assert os.path.exists(path)

    # Ensure the file can be compiled and tested
    result = subprocess.run(["forge", "test", "--match-contract", "DynamicArrays_Echidna_Test"], capture_output=True, text=True, check=False)
    output = result.stdout

    # Remove ansi escape sequences
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    result = ansi_escape.sub('', output)

    # Ensure all tests fail
    match = re.search(PATTERN, result)
    if match:
        tests_passed = int(match.group(2))
        assert tests_passed == 0
    else:
        assert False, "No tests were ran"

def test_echidna_structs_and_enums(structs_and_enums):
    structs_and_enums.echidna_generate_tests()
    # Ensure the file was created
    path = os.path.join(os.getcwd(), "test", "TupleTypes_Echidna_Test.t.sol")
    assert os.path.exists(path)

    # Ensure the file can be compiled and tested
    result = subprocess.run(["forge", "test", "--match-contract", "TupleTypes_Echidna_Test"], capture_output=True, text=True, check=False)
    output = result.stdout

    # Remove ansi escape sequences
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    result = ansi_escape.sub('', output)

    # Ensure all tests fail
    match = re.search(PATTERN, result)
    if match:
        tests_passed = int(match.group(2))
        assert tests_passed == 0
    else:
        assert False, "No tests were ran"