"""Defines the flags and logic associated with the `init` command"""
import json
from argparse import Namespace, ArgumentParser
from fuzz_utils.utils.crytic_print import CryticPrint
from fuzz_utils.templates.default_config import default_config


def init_flags(parser: ArgumentParser) -> None:  # pylint: disable=unused-argument
    """The `init` command flags"""
    # No flags are defined for the `init` command
    return None


def init_command(args: Namespace) -> None:  # pylint: disable=unused-argument
    """The execution logic of the `init` command"""
    with open("fuzz-utils.json", "w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(default_config))
    CryticPrint().print_information("Initial config file saved to fuzz-utils.json")
