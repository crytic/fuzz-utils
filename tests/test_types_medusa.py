""" Tests for generating compilable test files from an Medusa corpus"""
from pathlib import Path
import pytest
from pytest import TempPathFactory

from .conftest import TestGenerator, run_generation_command_test

TEST_DATA_DIR = Path(__file__).resolve().parent / "test_data"
PATTERN = r"(\d+)\s+failing tests,\s+(\d+)\s+tests succeeded"


def test_medusa_basic_types(
    setup_foundry_temp_dir: TempPathFactory,  # pylint: disable=unused-argument
    basic_types: TestGenerator,
) -> None:
    """Tests the BasicTypes contract with a Medusa corpus"""
    run_generation_command_test(basic_types.medusa_generate_tests, "BasicTypes", "Medusa", PATTERN)


def test_medusa_fixed_array_types(
    setup_foundry_temp_dir: TempPathFactory,  # pylint: disable=unused-argument
    fixed_size_arrays: TestGenerator,
) -> None:
    """Tests the FixedArrays contract with a Medusa corpus"""
    run_generation_command_test(
        fixed_size_arrays.medusa_generate_tests, "FixedArrays", "Medusa", PATTERN
    )


def test_medusa_dynamic_array_types(
    setup_foundry_temp_dir: TempPathFactory,  # pylint: disable=unused-argument
    dynamic_arrays: TestGenerator,
) -> None:
    """Tests the DynamicArrays contract with a Medusa corpus"""
    run_generation_command_test(
        dynamic_arrays.medusa_generate_tests, "DynamicArrays", "Medusa", PATTERN
    )


def test_medusa_structs_and_enums(
    setup_foundry_temp_dir: TempPathFactory,  # pylint: disable=unused-argument
    structs_and_enums: TestGenerator,
) -> None:
    """Tests the TupleTypes contract with a Medusa corpus"""
    run_generation_command_test(
        structs_and_enums.medusa_generate_tests, "TupleTypes", "Medusa", PATTERN
    )


@pytest.mark.xfail(strict=True)  # type: ignore[misc]
def test_medusa_value_transfer(
    setup_foundry_temp_dir: TempPathFactory,  # pylint: disable=unused-argument
    value_transfer: TestGenerator,
) -> None:
    """Tests the ValueTransfer contract with a Medusa corpus"""
    run_generation_command_test(
        value_transfer.medusa_generate_tests, "ValueTransfer", "Medusa", PATTERN
    )
