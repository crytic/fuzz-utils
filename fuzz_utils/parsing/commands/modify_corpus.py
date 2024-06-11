"""Defines the flags and logic associated with the `modify-corpus` command"""
from argparse import Namespace, ArgumentParser
from slither import Slither
from fuzz_utils.utils.crytic_print import CryticPrint
from fuzz_utils.modify_corpus.CorpusModifier import CorpusModifier
from fuzz_utils.utils.error_handler import handle_exit
from fuzz_utils.parsing.parser_util import check_config_and_set_default_values, open_config

COMMAND: str = "modify-corpus"


def modify_flags(parser: ArgumentParser) -> None:
    """The unit test generation parser flags"""
    parser.add_argument(
        "compilation_path", help="Path to the Echidna/Medusa test harness or Foundry directory."
    )
    parser.add_argument(
        "-cd", "--corpus-dir", dest="corpus_dir", help="Path to the corpus directory"
    )
    parser.add_argument(
        "-f",
        "--fuzzer",
        dest="selected_fuzzer",
        help="Define the fuzzer used. Valid inputs: 'echidna', 'medusa'",
    )
    parser.add_argument(
        "--fuzzer-config",
        dest="fuzzer_config",
        help="Define the location of the fuzzer config file.",
    )
    # TODO add specific commands for modifying the corpus


# pylint: disable=too-many-branches
def modify_command(args: Namespace) -> None:
    """The execution logic of the `modify-corpus` command"""
    config: dict = {}

    # If the config file is defined, read it
    if args.config:
        config = open_config(args.config, COMMAND)
    # Override the config with the CLI values
    if args.compilation_path:
        config["compilationPath"] = args.compilation_path
    if args.selected_fuzzer:
        config["fuzzer"] = args.selected_fuzzer.lower()
    if args.corpus_dir:
        config["corpusDir"] = args.corpus_dir
    if args.fuzzer_config:
        config["fuzzerConfig"] = args.fuzzer_config

    check_config_and_set_default_values(
        config,
        ["compilationPath", "fuzzer", "corpusDir"],
        [".", "echidna", "corpus"],
    )

    CryticPrint().print_information("Running Slither...")
    slither = Slither(args.compilation_path)

    derive_config(slither, config)

    if config["fuzzer"] not in {"echidna", "medusa"}:
        handle_exit(
                f"\n* The requested fuzzer {config['fuzzer']} is not supported. Supported fuzzers: echidna, medusa."
            )

    corpus_modifier = CorpusModifier(config["fuzzerConfig"], config["corpusDir"], slither, config["fuzzer"])
    corpus_modifier.modify_corpus()

    CryticPrint().print_success("Done!")


def derive_config(slither: Slither, config: dict) -> None:
    """Derive values for the target contract and inheritance path"""
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
