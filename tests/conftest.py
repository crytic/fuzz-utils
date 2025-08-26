""" Globally available fixtures"""
import os
import subprocess
import re
import shutil
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
            "inheritancePath": f"../src/{target}.sol",
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


@pytest.fixture()  # type: ignore[misc]
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


@pytest.fixture(scope="session")  # type: ignore[misc]
def setup_foundry_temp_dir(tmp_path_factory: Any) -> Any:
    """Sets up a temporary directory for the tests that contain all the necessary Foundry files"""
    # Create a temporary directory valid for the session
    temp_dir = tmp_path_factory.mktemp("foundry_session")
    original_dir: str = os.getcwd()

    print("Installing Forge...")
    subprocess.run(["forge", "init", "--no-git"], check=True, cwd=temp_dir)
    subprocess.run(["forge", "install", "crytic/properties", "--no-git"], check=True, cwd=temp_dir)
    subprocess.run(
        ["forge", "install", "transmissions11/solmate", "--no-git"], check=True, cwd=temp_dir
    )

    # Create foundry config
    foundry_config = os.path.join(temp_dir, "foundry.toml")
    out_str: str = '[profile.default]\nsolc-version = "0.8.19"\nevm_version = "shanghai"'
    with open(foundry_config, "w", encoding="utf-8") as outfile:
        outfile.write(out_str)

    # Create remappings file
    create_remappings_file(temp_dir, None)

    # Delete unnecessary files
    counter_path = temp_dir / "src" / "Counter.sol"
    counter_path.unlink()
    assert not counter_path.exists()

    counter_test_path = temp_dir / "test" / "Counter.t.sol"
    counter_test_path.unlink()
    assert not counter_test_path.exists()

    scripts_dir = temp_dir / "script"
    shutil.rmtree(scripts_dir)
    assert not scripts_dir.exists()

    # Create the corpora directories in the temporary dir
    echidna_corpora_dir = temp_dir / "echidna-corpora"
    medusa_corpora_dir = temp_dir / "medusa-corpora"
    echidna_corpora_dir.mkdir(exist_ok=True)
    medusa_corpora_dir.mkdir(exist_ok=True)

    # Copy all our contracts and corpora to the temporary directory
    copy_directory_contents(
        os.path.join(original_dir, "tests", "test_data", "echidna-corpora"),
        temp_dir / "echidna-corpora",
    )
    copy_directory_contents(
        os.path.join(original_dir, "tests", "test_data", "medusa-corpora"),
        temp_dir / "medusa-corpora",
    )
    copy_directory_contents(
        os.path.join(original_dir, "tests", "test_data", "src"), temp_dir / "src"
    )

    os.chdir(temp_dir)
    return temp_dir


def create_file(temp_dir: Any, file_name: str, out_str: str) -> None:
    """Creates a remappings file"""
    file_path = os.path.join(temp_dir, file_name)
    with open(file_path, "w", encoding="utf-8") as outfile:
        outfile.write(out_str)


def create_remappings_file(temp_dir: Any, out_str: str | None) -> None:
    """Creates a remappings file"""
    if not out_str:
        out_str = "forge-std/=lib/forge-std/src/\nproperties/=lib/properties/contracts/\nsolmate/=lib/solmate/src/\nsrc/=src/"

    create_file(temp_dir, "remappings.txt", out_str)


def copy_directory_contents(src_dir: str, dest_dir: str) -> None:
    """
    Copies the contents of src_dir into dest_dir. The dest_dir must already exist.
    Directories under src_dir will be created under dest_dir and files will be copied.
    """
    for item in os.listdir(src_dir):
        s = os.path.join(src_dir, item)
        d = os.path.join(dest_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)  # For Python 3.8+, use dirs_exist_ok=True
        else:
            shutil.copy2(s, d)


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
