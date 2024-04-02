"""Utility functions used in the command parsers"""
import json
from fuzz_utils.utils.error_handler import handle_exit


def check_config_and_set_default_values(
    config: dict, fields: list[str], defaults: list[str]
) -> None:
    """Checks that the configuration dictionary contains a non-empty field"""
    assert len(fields) == len(defaults)
    for idx, field in enumerate(fields):
        if field not in config or len(config[field]) == 0:
            config[field] = defaults[idx]


def check_configuration_field_exists_and_non_empty(config: dict, command: str, field: str) -> None:
    """Checks that the configuration dictionary contains a non-empty field"""
    if field not in config or len(config[field]) == 0:
        handle_exit(f"The {command} configuration field {field} is not configured.")


def open_config(cli_config: str, command: str) -> dict:
    """Open config file if provided return its contents"""
    with open(cli_config, "r", encoding="utf-8") as readFile:
        complete_config = json.load(readFile)
        if command in complete_config:
            return complete_config[command]

        handle_exit(
            f"The provided configuration file does not contain the `{command}` command configuration field."
        )
