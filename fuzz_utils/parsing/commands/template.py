"""Defines the flags and logic associated with the `template` command"""
import os
import json
from argparse import Namespace, ArgumentParser
from slither import Slither
from fuzz_utils.template.HarnessGenerator import HarnessGenerator
from fuzz_utils.utils.crytic_print import CryticPrint
from fuzz_utils.utils.remappings import find_remappings


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
    config["outputDir"] = output_dir

    CryticPrint().print_information("Running Slither...")
    slither = Slither(config["compilationPath"])

    # Check if dependencies are installed
    include_attacks = bool("attacks" in config and len(config["attacks"]) > 0)
    remappings = find_remappings(include_attacks)

    generator = HarnessGenerator(config, slither, remappings)
    generator.generate_templates()
