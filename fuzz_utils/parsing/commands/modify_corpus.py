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
    parser.add_argument("-c", "--contract", dest="target_contract", help="Define the contract name")
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
    parser.add_argument(
        "--mode",
        dest="filter_mode",
        help="Define how the corpus will me modified. Available options are: `delete_sequence` and `delete_calls`",
    )
    parser.add_argument(
        "--modify-senders",
        dest="modify_senders",
        nargs="+",
        help="Define sender remappings in the format `0xoldSender=0xnewSender,0xold2=0xnew2,...`",
    )
    parser.add_argument(
        "-ff",
        "--filter-functions",
        dest="filter_functions",
        help="Remove functions that no longer exist from the corpus.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "-dr",
        "--dry-run",
        dest="dry_run",
        help="Print out any corpus calls that would be modified.",
        default=False,
        action="store_true",
    )
    # TODO add specific commands for modifying the corpus


# pylint: disable=too-many-branches
def modify_command(args: Namespace) -> None:
    """The execution logic of the `modify-corpus` command"""
    config: dict = {}

    # Override the config with the CLI values
    if args.compilation_path:
        config["compilationPath"] = args.compilation_path
    if args.target_contract:
        config["targetContract"] = args.target_contract
    if args.selected_fuzzer:
        config["fuzzer"] = args.selected_fuzzer.lower()
    if args.corpus_dir:
        config["corpusDir"] = args.corpus_dir
    if args.fuzzer_config:
        config["fuzzerConfigPath"] = args.fuzzer_config
    if args.filter_mode:
        config["mode"] = args.filter_mode
    if args.modify_senders:
        config["modifySenders"] = {}
        # Process list
        for item in args.modify_senders:
            assert("=" in item)
            senders = item.split("=")
            config["modifySenders"][senders[0]] = senders[1]
    if args.filter_functions:
        config["filterFunctions"] = args.filter_functions
    if args.dry_run:
        config["dryRun"] = args.dry_run
        CryticPrint().print_error("The --dry-run command isn't implemented yet, come back in a bit!")

    check_config_and_set_default_values(
        config,
        ["compilationPath", "fuzzer", "corpusDir", "mode"],
        [".", "echidna", "corpus", "filter_calls"],
    )

    CryticPrint().print_information("Running Slither...")
    slither = Slither(args.compilation_path)

    derive_config(slither, config)

    if config["fuzzer"] not in {"echidna", "medusa"}:
        handle_exit(
                f"\n* The requested fuzzer {config['fuzzer']} is not supported. Supported fuzzers: echidna, medusa."
            )

    corpus_modifier = CorpusModifier(config, slither)
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
