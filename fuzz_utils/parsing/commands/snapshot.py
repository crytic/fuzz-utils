"""Defines the flags and logic associated with the `modify-corpus` command"""
from argparse import Namespace, ArgumentParser
from fuzz_utils.utils.crytic_print import CryticPrint
from fuzz_utils.modify_corpus.CorpusModifier import CorpusModifier
from fuzz_utils.utils.error_handler import handle_exit
from fuzz_utils.parsing.parser_util import check_config_and_set_default_values

COMMAND: str = "modify-corpus"


def snapshot_flags(parser: ArgumentParser) -> None:
    """The unit test generation parser flags"""
    parser.add_argument(
        "-cd", "--corpus-dir", dest="corpus_dir", help="Path to the corpus directory"
    )
    parser.add_argument(
        "-f",
        "--fuzzer",
        dest="selected_fuzzer",
        help="Define the fuzzer used. Valid inputs: 'echidna', 'medusa'",
    )


# pylint: disable=too-many-branches
def snapshot_command(args: Namespace) -> None:
    """The execution logic of the `snapshot` command"""
    config: dict = {}

    if args.corpus_dir:
        config["corpusDir"] = args.corpus_dir
    if args.selected_fuzzer:
        config["fuzzer"] = args.selected_fuzzer.lower()
        if config["fuzzer"] not in {"echidna", "medusa"}:
            handle_exit(f"The provided fuzzer {config['fuzzer']} is not supported.")

    check_config_and_set_default_values(
        config,
        ["fuzzer", "corpusDir"],
        ["echidna", "corpus"],
    )

    corpus_modifier = CorpusModifier(None, config["corpusDir"], None, config["fuzzer"])
    corpus_modifier.save_corpus_to_history()
