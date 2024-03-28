""" Tests for generating compilable test files from an Echidna corpus"""
from pathlib import Path
from pytest import TempPathFactory
from .conftest import TestGenerator, run_generation_command_test


TEST_DATA_DIR = Path(__file__).resolve().parent / "test_data"
PATTERN = r"(\d+)\s+failing tests,\s+(\d+)\s+tests succeeded"


def test_echidna_basic_types(
    setup_foundry_temp_dir: TempPathFactory,  # pylint: disable=unused-argument
    basic_types: TestGenerator,
) -> None:
    """Tests the BasicTypes contract with an Echidna corpus"""
    run_generation_command_test(
        basic_types.echidna_generate_tests, "BasicTypes", "Echidna", PATTERN
    )


def test_echidna_fixed_array_types(
    setup_foundry_temp_dir: TempPathFactory,  # pylint: disable=unused-argument
    fixed_size_arrays: TestGenerator,
) -> None:
    """Tests the FixedArrays contract with an Echidna corpus"""
    run_generation_command_test(
        fixed_size_arrays.echidna_generate_tests, "FixedArrays", "Echidna", PATTERN
    )


def test_echidna_dynamic_array_types(
    setup_foundry_temp_dir: TempPathFactory,  # pylint: disable=unused-argument
    dynamic_arrays: TestGenerator,
) -> None:
    """Tests the DynamicArrays contract with an Echidna corpus"""
    run_generation_command_test(
        dynamic_arrays.echidna_generate_tests, "DynamicArrays", "Echidna", PATTERN
    )


def test_echidna_structs_and_enums(
    setup_foundry_temp_dir: TempPathFactory,  # pylint: disable=unused-argument
    structs_and_enums: TestGenerator,
) -> None:
    """Tests the TupleTypes contract with an Echidna corpus"""
    run_generation_command_test(
        structs_and_enums.echidna_generate_tests, "TupleTypes", "Echidna", PATTERN
    )


def test_echidna_value_transfer(
    setup_foundry_temp_dir: TempPathFactory,  # pylint: disable=unused-argument
    value_transfer: TestGenerator,
) -> None:
    """Tests the ValueTransfer contract with an Echidna corpus"""
    run_generation_command_test(
        value_transfer.echidna_generate_tests, "ValueTransfer", "Echidna", PATTERN
    )
