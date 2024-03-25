""" Generates a test file from Echidna reproducers """
import sys
import argparse
from fuzz_utils.parsing.parser import define_subparsers, run_command

# pylint: disable=too-many-locals,too-many-statements
def main() -> None:  # type: ignore[func-returns-value]
    """The main entry point"""
    parser = argparse.ArgumentParser(
        prog="fuzz-utils", description="Generate test harnesses for Echidna failed properties."
    )
    subparsers = parser.add_subparsers(dest="command", help="sub-command help")
    define_subparsers(subparsers)
    args = parser.parse_args()
    command_success: bool = run_command(args)
    if not command_success:
        parser.print_help()


if __name__ == "__main__":
    sys.exit(main())  # type: ignore[func-returns-value]
