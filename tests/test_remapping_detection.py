"""Remapping detection unit tests"""
import os
from typing import Any
import pytest
from fuzz_utils.utils.remappings import find_remappings
from .conftest import create_remappings_file


def test_remappings_are_detected_when_no_file(
    setup_foundry_temp_dir: Any,  # pylint: disable=unused-argument
) -> None:
    """Test if remappings are fetched when no remappings.txt file exists"""
    temp_dir = os.getcwd()

    # Remove remappings file
    remappings_path = os.path.join(temp_dir, "remappings.txt")
    os.remove(remappings_path)
    assert not os.path.exists(remappings_path)

    # Look for remappings, expecting not to fail
    try:
        find_remappings(True)
    except SystemExit:
        # Re-create remappings file and raise error
        create_remappings_file(temp_dir)
        pytest.fail("Finding remappings failed with SystemExit")
    except Exception:  # pylint: disable=broad-except
        # Re-create remappings file and raise error
        create_remappings_file(temp_dir)
        pytest.fail("Finding remappings failed with an Exception")

    # If success
    create_remappings_file(temp_dir)


def test_remappings_are_detected_when_file_exists(
    setup_foundry_temp_dir: Any,  # pylint: disable=unused-argument
) -> None:
    """Test if remappings are fetched when a remappings.txt file exists"""
    temp_dir = os.getcwd()
    assert os.path.exists(os.path.join(temp_dir, "remappings.txt"))
    find_remappings(True)
