""" Utility function for error handling"""
import sys
from typing import NoReturn
from fuzz_utils.utils.crytic_print import CryticPrint


def handle_exit(reason: str) -> NoReturn:
    """Print an error message to the console and exit"""
    CryticPrint().print_error(reason)
    sys.exit()
