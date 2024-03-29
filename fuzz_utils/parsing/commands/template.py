"""Defines the flags and logic associated with the `template` command"""
import os
import json
from argparse import Namespace, ArgumentParser
from slither import Slither
from fuzz_utils.template.HarnessGenerator import HarnessGenerator
from fuzz_utils.utils.crytic_print import CryticPrint
from fuzz_utils.utils.remappings import find_remappings
from fuzz_utils.utils.error_handler import handle_exit


def template_flags(parser: ArgumentParser) -> None:
    """The harness template generation parser flags"""
    parser.add_argument("compilation_path", help="Path to the Solidity contract.")
    parser.add_argument("-n", "--name", dest="name", help="Name of the harness contract.")
    parser.add_argument(
        "-c",
        "--contracts",
        dest="target_contracts",
        nargs="+",
        help="Define a list of target contracts for the harness.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        dest="output_dir",
        help="Define the output directory where the result will be saved.",
    )
    parser.add_argument("--config", dest="config", help="Define the location of the config file.")
    parser.add_argument(
        "--mode",
        dest="mode",
        help="Define the harness generation strategy you want to use. Valid options are `simple`, `prank`, `actor`",
    )


def template_command(args: Namespace) -> None:
    """The execution logic of the `generate` command"""
    config: dict = {}
    if args.output_dir:
        output_dir = os.path.join("./test", args.output_dir)
    else:
        output_dir = os.path.join("./test", "fuzzing")
    if args.config:
        with open(args.config, "r", encoding="utf-8") as readFile:
            complete_config = json.load(readFile)
            if "template" in complete_config:
                config = complete_config["template"]

    if args.target_contracts:
        config["targets"] = args.target_contracts
    if args.compilation_path:
        config["compilationPath"] = args.compilation_path
    if args.name:
        config["name"] = args.name
    if args.mode:
        config["mode"] = args.mode.lower()
    config["outputDir"] = output_dir

    CryticPrint().print_information("Running Slither...")
    slither = Slither(config["compilationPath"])

    # Check if dependencies are installed
    include_attacks = bool("attacks" in config and len(config["attacks"]) > 0)
    remappings = find_remappings(include_attacks)

    generator = HarnessGenerator(config, slither, remappings)
    generator.generate_templates()


def check_configuration(config: dict) -> None:
    """Checks the configuration"""
    mandatory_configuration_fields = ["mode", "targets", "compilationPath"]
    for field in mandatory_configuration_fields:
        check_configuration_field_exists_and_non_empty(config, field)

    if config["mode"].lower() not in ("simple", "prank", "actor"):
        handle_exit(
            f"The selected mode {config['mode']} is not a valid harness generation strategy."
        )


def check_configuration_field_exists_and_non_empty(config: dict, field: str) -> None:
    """Checks that the configuration dictionary contains a non-empty field"""
    if field not in config or len(config[field]) == 0:
        handle_exit(f"The template configuration field {field} is not configured.")
