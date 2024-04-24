"""Remapping detection unit tests"""
import os
from typing import Any
import pytest
from slither import Slither
from fuzz_utils.utils.remappings import find_remappings
from .conftest import create_remappings_file


def test_remappings_are_detected_when_no_file(
    setup_foundry_temp_dir: Any,  # pylint: disable=unused-argument
) -> None:
    """Test if remappings are fetched when no remappings.txt file exists"""
    temp_dir = os.getcwd()
    slither = Slither(temp_dir)

    # Remove remappings file
    remappings_path = os.path.join(temp_dir, "remappings.txt")
    os.remove(remappings_path)
    assert not os.path.exists(remappings_path)

    # Look for remappings, expecting not to fail
    try:
        find_remappings(True, slither)
    except SystemExit:
        # Re-create remappings file and raise error
        create_remappings_file(temp_dir, None)
        pytest.fail("Finding remappings failed with SystemExit")
    except Exception:  # pylint: disable=broad-except
        # Re-create remappings file and raise error
        create_remappings_file(temp_dir, None)
        pytest.fail("Finding remappings failed with an Exception")

    # If success
    create_remappings_file(temp_dir, None)


def test_remappings_are_detected_when_file_exists(
    setup_foundry_temp_dir: Any,  # pylint: disable=unused-argument
) -> None:
    """Test if remappings are fetched when a remappings.txt file exists"""
    temp_dir = os.getcwd()
    slither = Slither(temp_dir)
    assert os.path.exists(os.path.join(temp_dir, "remappings.txt"))
    find_remappings(True, slither)


def test_remappings_are_detected_when_incomplete_remappings_file(
    setup_foundry_temp_dir: Any,  # pylint: disable=unused-argument
) -> None:
    """Test if remappings are fetched when a remappings.txt file exists but is incomplete"""
    temp_dir = os.getcwd()
    slither = Slither(temp_dir)

    # Modify remappings file to contain an incomplete list of remappings
    out_str = "forge-std/=lib/forge-std/src/\nsolmate/=lib/solmate/src/\nsrc/=src/"
    create_remappings_file(temp_dir, out_str)

    # Look for remappings, expecting not to fail
    try:
        find_remappings(True, slither)
    except SystemExit:
        # Reset remappings file and raise error
        create_remappings_file(temp_dir, None)
        pytest.fail("Finding remappings failed with SystemExit")
    except Exception:  # pylint: disable=broad-except
        # Reset remappings file and raise error
        create_remappings_file(temp_dir, None)
        pytest.fail("Finding remappings failed with an Exception")

    # If success, reset remappings file
    create_remappings_file(temp_dir, None)


def test_remappings_are_detected_when_file_target(
    setup_foundry_temp_dir: Any,  # pylint: disable=unused-argument
) -> None:
    """Test if remappings are fetched when the slither target is a .sol file"""
    temp_dir = os.getcwd()
    file_path = os.path.join(temp_dir, "src", "BasicTypes.sol")
    slither = Slither(file_path)

    # Modify remappings file to contain an incomplete list of remappings
    out_str = "forge-std/=lib/forge-std/src/\nsolmate/=lib/solmate/src/\nsrc/=src/"
    create_remappings_file(temp_dir, out_str)

    # Look for remappings, expecting not to fail
    try:
        find_remappings(True, slither)
    except SystemExit:
        # Reset remappings file and raise error
        create_remappings_file(temp_dir, None)
        pytest.fail("Finding remappings failed with SystemExit")
    except Exception:  # pylint: disable=broad-except
        # Reset remappings file and raise error
        create_remappings_file(temp_dir, None)
        pytest.fail("Finding remappings failed with an Exception")

    # If success, reset remappings file
    create_remappings_file(temp_dir, None)
