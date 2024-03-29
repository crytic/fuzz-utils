""" Tests for generating fuzzing harnesses"""
from pathlib import Path
import copy
import subprocess
from pytest import TempPathFactory
from slither import Slither
from slither.core.declarations.contract import Contract
from slither.core.declarations.function_contract import FunctionContract
from fuzz_utils.utils.remappings import find_remappings

from fuzz_utils.template.HarnessGenerator import HarnessGenerator

TEST_DATA_DIR = Path(__file__).resolve().parent / "test_data"
default_config = {
    "name": "DefaultHarness",
    "compilationPath": ".",
    "targets": [],
    "outputDir": "./test/fuzzing",
    "actors": [
        {
            "name": "Default",
            "targets": [],
            "number": 3,
            "filters": {
                "strict": False,
                "onlyModifiers": [],
                "onlyPayable": False,
                "onlyExternalCalls": [],
            },
        }
    ],
    "attacks": [],
}


def test_modifier_filtering(
    setup_foundry_temp_dir: TempPathFactory,  # pylint: disable=unused-argument
) -> None:
    """Test non-strict modifier filtering"""
    filters = {
        "strict": False,
        "onlyModifiers": ["onlyOwner"],
        "onlyPayable": False,
        "onlyExternalCalls": [],
    }
    expected_functions = set(["iAmRestricted"])
    run_harness(
        "ModifierHarness",
        "Modifier",
        "./src/Filtering.sol",
        ["Filtering"],
        filters,
        expected_functions,
    )


def test_external_call_filtering(
    setup_foundry_temp_dir: TempPathFactory,  # pylint: disable=unused-argument
) -> None:
    """Test non-strict external call filtering"""
    filters = {
        "strict": False,
        "onlyModifiers": [],
        "onlyPayable": False,
        "onlyExternalCalls": ["transferFrom"],
    }
    expected_functions = set(["depositWithModifier", "depositNoModifier"])
    run_harness(
        "TransferHarness",
        "Transfer",
        "./src/Filtering.sol",
        ["Filtering"],
        filters,
        expected_functions,
    )


def test_payable_filtering(
    setup_foundry_temp_dir: TempPathFactory,  # pylint: disable=unused-argument
) -> None:
    """Test non-strict payable call filtering"""
    filters = {
        "strict": False,
        "onlyModifiers": [],
        "onlyPayable": True,
        "onlyExternalCalls": [],
    }
    expected_functions = set(["iAmPayable"])
    run_harness(
        "PayableHarness",
        "Payable",
        "./src/Filtering.sol",
        ["Filtering"],
        filters,
        expected_functions,
    )


def test_modifier_and_external_call_filtering(
    setup_foundry_temp_dir: TempPathFactory,  # pylint: disable=unused-argument
) -> None:
    """Test non-strict modifier and external call filtering"""
    filters = {
        "strict": False,
        "onlyModifiers": ["enforceTransferFrom"],
        "onlyPayable": False,
        "onlyExternalCalls": ["transferFrom"],
    }
    expected_functions = set(["depositWithModifier", "depositNoModifier"])
    run_harness(
        "ModExHarness",
        "ModEx",
        "./src/Filtering.sol",
        ["Filtering"],
        filters,
        expected_functions,
    )


def test_strict_modifier_and_external_call_filtering(
    setup_foundry_temp_dir: TempPathFactory,  # pylint: disable=unused-argument
) -> None:
    """Test strict modifier and external call filtering"""
    filters = {
        "strict": True,
        "onlyModifiers": ["enforceTransferFrom"],
        "onlyPayable": False,
        "onlyExternalCalls": ["transferFrom"],
    }
    expected_functions = set(["depositWithModifier"])
    run_harness(
        "StrictModExHarness",
        "StrictModEx",
        "./src/Filtering.sol",
        ["Filtering"],
        filters,
        expected_functions,
    )


def test_multiple_external_calls_filtering(
    setup_foundry_temp_dir: TempPathFactory,  # pylint: disable=unused-argument
) -> None:
    """Test multiple external calls filtering"""
    filters = {
        "strict": True,
        "onlyModifiers": [],
        "onlyPayable": False,
        "onlyExternalCalls": ["transferFrom", "transfer"],
    }
    expected_functions = set(["depositWithModifier", "depositNoModifier", "withdraw"])
    run_harness(
        "MulExHarness",
        "MulEx",
        "./src/Filtering.sol",
        ["Filtering"],
        filters,
        expected_functions,
    )


def test_strict_multiple_external_calls_filtering(
    setup_foundry_temp_dir: TempPathFactory,  # pylint: disable=unused-argument
) -> None:
    """Test strict multiple external calls filtering"""
    filters = {
        "strict": True,
        "onlyModifiers": [],
        "onlyPayable": False,
        "onlyExternalCalls": ["transferFrom", "transfer"],
    }
    expected_functions = set(["depositWithModifier", "depositNoModifier", "withdraw"])
    run_harness(
        "StrictMulExHarness",
        "StrictMulEx",
        "./src/Filtering.sol",
        ["Filtering"],
        filters,
        expected_functions,
    )


def run_harness(
    harness_name: str,
    actor_name: str,
    compilation_path: str,
    targets: list,
    filters: dict,
    expected_functions: set[str],
) -> None:
    """Sets up the HarnessGenerator"""
    remappings = find_remappings(False)
    config = copy.deepcopy(default_config)
    slither = Slither(compilation_path)

    config["name"] = harness_name
    config["compilationPath"] = compilation_path
    config["targets"] = targets
    config["actors"][0]["filters"] = filters  # type: ignore[index]
    config["actors"][0]["name"] = actor_name  # type: ignore[index]

    generator = HarnessGenerator(config, slither, remappings)
    generator.generate_templates()

    # Ensure the file can be compiled
    subprocess.run(["forge", "build", "--build-info"], capture_output=True, text=True, check=True)

    # Ensure the harness only contains the functions we're expecting
    slither = Slither(f"./test/fuzzing/harnesses/{harness_name}.sol")
    target: Contract = generator.get_target_contract(slither, harness_name)
    compare_with_declared_functions(target, set(expected_functions))


def compare_with_declared_functions(target: Contract, expected: set) -> None:
    """Compare expected functions set with declared set"""
    declared: set = {entry.name for entry in target.functions_declared if include_function(entry)}
    assert declared == expected


def include_function(function: FunctionContract) -> bool:
    """Determines if a function should be included or not"""
    if (
        function.pure
        or function.view
        or function.is_constructor
        or function.is_fallback
        or function.is_receive
    ):
        return False
    return True
