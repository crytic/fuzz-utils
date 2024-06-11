"""Defines the flags and logic associated with the `modify-corpus` command"""
from argparse import Namespace, ArgumentParser
from fuzz_utils.utils.crytic_print import CryticPrint
from fuzz_utils.modify_corpus.CorpusModifier import CorpusModifier
from fuzz_utils.utils.error_handler import handle_exit

COMMAND: str = "modify-corpus"


def restore_flags(parser: ArgumentParser) -> None:
    """The unit test generation parser flags"""
    parser.add_argument(
        "-ch", "--hash", dest="corpus_hash", help="Hash of the historic corpus that will be restored."
    )
    parser.add_argument(
        "-lh",
        "--list-history",
        dest="list_history",
        help="List the corpora that are saved in history.",
        default=False,
        action="store_true",
    )


# pylint: disable=too-many-branches
def restore_command(args: Namespace) -> None:
    """The execution logic of the `restore` command"""

    corpus_modifier = CorpusModifier(None, None, None, None)
    # Override the config with the CLI values
    if args.list_history:
        corpus_modifier.list_historic_corpora()
    else:
        if args.corpus_hash:
            corpus_modifier.restore_corpus_from_history(args.corpus_hash)
        else:
            handle_exit("No hash was provided!")