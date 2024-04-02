"""Defines the flags and logic associated with the `generate` command"""
from pathlib import Path
from argparse import Namespace, ArgumentParser
from slither import Slither
from fuzz_utils.utils.crytic_print import CryticPrint
from fuzz_utils.generate.FoundryTest import FoundryTest
from fuzz_utils.generate.fuzzers.Medusa import Medusa
from fuzz_utils.generate.fuzzers.Echidna import Echidna
from fuzz_utils.utils.error_handler import handle_exit
from fuzz_utils.parsing.parser_util import check_config_and_set_default_values, open_config
from fuzz_utils.utils.slither_utils import get_target_contract

COMMAND: str = "generate"


def generate_flags(parser: ArgumentParser) -> None:
    """The unit test generation parser flags"""
    parser.add_argument(
        "compilation_path", help="Path to the Echidna/Medusa test harness or Foundry directory."
    )
    parser.add_argument(
        "-cd", "--corpus-dir", dest="corpus_dir", help="Path to the corpus directory"
    )
    parser.add_argument("-c", "--contract", dest="target_contract", help="Define the contract name")
    parser.add_argument(
        "-td",
        "--test-directory",
        dest="test_directory",
        help="Define the directory that contains the Foundry tests.",
    )
    parser.add_argument(
        "-i",
        "--inheritance-path",
        dest="inheritance_path",
        help="Define the relative path from the test directory to the directory src/contracts directory.",
    )
    parser.add_argument(
        "-f",
        "--fuzzer",
        dest="selected_fuzzer",
        help="Define the fuzzer used. Valid inputs: 'echidna', 'medusa'",
    )
    parser.add_argument(
        "--named-inputs",
        dest="named_inputs",
        help="Include function input names when making calls.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--config",
        dest="config",
        help="Define the location of the config file.",
    )
    parser.add_argument(
        "--all-sequences",
        dest="all_sequences",
        help="Include all corpus sequences when generating unit tests.",
        default=False,
        action="store_true",
    )


# pylint: disable=too-many-branches
def generate_command(args: Namespace) -> None:
    """The execution logic of the `generate` command"""
    config: dict = {}
    # If the config file is defined, read it
    if args.config:
        config = open_config(args.config, COMMAND)
    # Override the config with the CLI values
    if args.compilation_path:
        config["compilationPath"] = args.compilation_path
    if args.test_directory:
        config["testsDir"] = args.test_directory
    if args.inheritance_path:
        config["inheritancePath"] = args.inheritance_path
    if args.selected_fuzzer:
        config["fuzzer"] = args.selected_fuzzer.lower()
    if args.corpus_dir:
        config["corpusDir"] = args.corpus_dir
    if args.target_contract:
        config["targetContract"] = args.target_contract
    if args.named_inputs:
        config["namedInputs"] = args.named_inputs
    else:
        if "namedInputs" not in config:
            config["namedInputs"] = False
    if args.all_sequences:
        config["allSequences"] = args.all_sequences
    else:
        if "allSequences" not in config:
            config["allSequences"] = False

    check_config_and_set_default_values(
        config,
        ["compilationPath", "testsDir", "fuzzer", "corpusDir"],
        [".", "test", "medusa", "corpus"],
    )

    CryticPrint().print_information("Running Slither...")
    slither = Slither(args.compilation_path)
    fuzzer: Echidna | Medusa

    # Derive target if it is not defined but the compilationPath only contains one contract
    if "targetContract" not in config or len(config["targetContract"]) == 0:
        if len(slither.contracts_derived) == 1:
            config["targetContract"] = slither.contracts_derived[0].name
            CryticPrint().print_information(
                f"Target contract not specified. Using derived target: {config['targetContract']}."
            )
        else:
            handle_exit(
                "Target contract cannot be determined. Please specify the target with `-c targetName`"
            )

    # Derive inheritance path if it is not defined
    if "inheritancePath" not in config or len(config["inheritancePath"]) == 0:
        contract = get_target_contract(slither, config["targetContract"])
        contract_path = Path(contract.source_mapping.filename.relative)
        tests_path = Path(config["testsDir"])
        config["inheritancePath"] = str(
            Path(*([".." * len(tests_path.parts)])).joinpath(contract_path)
        )

    match config["fuzzer"]:
        case "echidna":
            fuzzer = Echidna(
                config["targetContract"], config["corpusDir"], slither, config["namedInputs"]
            )
        case "medusa":
            fuzzer = Medusa(
                config["targetContract"], config["corpusDir"], slither, config["namedInputs"]
            )
        case _:
            handle_exit(
                f"\n* The requested fuzzer {config['fuzzer']} is not supported. Supported fuzzers: echidna, medusa."
            )

    CryticPrint().print_information(
        f"Generating Foundry unit tests based on the {fuzzer.name} reproducers..."
    )
    foundry_test = FoundryTest(config, slither, fuzzer)
    foundry_test.create_poc()
    CryticPrint().print_success("Done!")
