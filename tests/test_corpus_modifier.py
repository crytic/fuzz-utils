""" Tests for generating compilable test files from an Echidna corpus"""
import os
import copy
from pathlib import Path
from pytest import TempPathFactory
from slither import Slither

from fuzz_utils.modify_corpus.CorpusModifier import CorpusModifier
from .conftest import create_file
from .modifier_expected_results import expected_results

TEST_DATA_DIR = Path(__file__).resolve().parent / "test_data"
default_config = {
    "compilationPath": ".",
    "corpusDir": "",
    "fuzzer": "",
    "fuzzerConfigPath": "",
    "targetContract": "BasicTypes",
    "mode": "",
    "modifySenders": {},
    "filterFunction": False,
    "dryRun": False,
}


def compare_corpus_with_expected(expected_corpus: list, new_corpus: list) -> None:
    """Compares two corpora, failing if they're not the same"""
    assert len(expected_corpus) == len(new_corpus)
    expected_corpus_sorted = sorted(expected_corpus, key=lambda d: d["name"])
    new_corpus_sorted = sorted(
        new_corpus, key=lambda d: os.path.normpath(d["path"]).split(os.path.sep)[-1]
    )
    for idx, item in enumerate(new_corpus_sorted):
        name = os.path.normpath(item["path"]).split(os.path.sep)[-1]
        assert expected_corpus_sorted[idx]["name"] == name
        assert expected_corpus_sorted[idx]["content"] == item["content"]


# delete_calls mode


def test_echidna_delay_delete_calls(
    setup_foundry_temp_dir: TempPathFactory,
) -> None:
    """Test that correct calls are deleted when filtering by time and block delay"""
    config = copy.deepcopy(default_config)
    config["mode"] = "delete_calls"
    config["corpusDir"] = "echidna-corpora/corpus-basic-modifier"
    config["fuzzerConfigPath"] = "echidna.yaml"
    config["fuzzer"] = "echidna"

    create_file(setup_foundry_temp_dir, "echidna.yaml", "maxTimeDelay: 65535\nmaxBlockDelay: 46801")

    modifier = CorpusModifier(config, None)
    new_corpus, corpus_hash = modifier.modify_corpus()

    modifier.restore_corpus_from_history(corpus_hash)
    compare_corpus_with_expected(expected_results["echidna"]["time_and_block_call"], new_corpus)


def test_echidna_blacklist_delete_calls(
    setup_foundry_temp_dir: TempPathFactory,
) -> None:
    """Test that correct calls are deleted when filtering blacklisted functions"""
    config = copy.deepcopy(default_config)
    config["mode"] = "delete_calls"
    config["corpusDir"] = "echidna-corpora/corpus-basic-modifier"
    config["fuzzerConfigPath"] = "echidna.yaml"
    config["fuzzer"] = "echidna"

    create_file(setup_foundry_temp_dir, "echidna.yaml", 'filterFunctions: ["check_uint256"]')

    modifier = CorpusModifier(config, None)
    new_corpus, corpus_hash = modifier.modify_corpus()

    modifier.restore_corpus_from_history(corpus_hash)
    compare_corpus_with_expected(
        expected_results["echidna"]["blacklisted_functions_call"], new_corpus
    )


def test_echidna_function_filter_delete_calls(
    setup_foundry_temp_dir: TempPathFactory,  # pylint: disable=unused-argument
) -> None:
    """Test that correct calls are deleted when filtering non-existent functions"""
    config = copy.deepcopy(default_config)
    config["corpusDir"] = "echidna-corpora/corpus-basic-modifier"
    config["targetContract"] = "BasicTypesNoCheckUint256"
    config["filterFunctions"] = True
    config["mode"] = "delete_calls"
    config["fuzzer"] = "echidna"

    slither = Slither(config["compilationPath"])
    modifier = CorpusModifier(config, slither)

    new_corpus, corpus_hash = modifier.modify_corpus()
    # print("new corpus", new_corpus)
    modifier.restore_corpus_from_history(corpus_hash)
    compare_corpus_with_expected(expected_results["echidna"]["invalid_functions_call"], new_corpus)


# delete_sequence mode


def test_echidna_delay_delete_sequence(
    setup_foundry_temp_dir: TempPathFactory,
) -> None:
    """Test that correct calls are deleted when filtering by time and block delay"""
    config = copy.deepcopy(default_config)
    config["mode"] = "delete_sequence"
    config["corpusDir"] = "echidna-corpora/corpus-basic-modifier"
    config["fuzzerConfigPath"] = "echidna.yaml"
    config["fuzzer"] = "echidna"

    create_file(setup_foundry_temp_dir, "echidna.yaml", "maxTimeDelay: 65535\nmaxBlockDelay: 46801")

    modifier = CorpusModifier(config, None)
    new_corpus, corpus_hash = modifier.modify_corpus()

    modifier.restore_corpus_from_history(corpus_hash)
    compare_corpus_with_expected(expected_results["echidna"]["time_and_block_seq"], new_corpus)


def test_echidna_blacklist_delete_sequence(
    setup_foundry_temp_dir: TempPathFactory,
) -> None:
    """Test that correct calls are deleted when filtering blacklisted functions"""
    config = copy.deepcopy(default_config)
    config["mode"] = "delete_sequence"
    config["corpusDir"] = "echidna-corpora/corpus-basic-modifier"
    config["fuzzerConfigPath"] = "echidna.yaml"
    config["fuzzer"] = "echidna"

    create_file(setup_foundry_temp_dir, "echidna.yaml", 'filterFunctions: ["check_uint256"]')

    modifier = CorpusModifier(config, None)
    new_corpus, corpus_hash = modifier.modify_corpus()

    modifier.restore_corpus_from_history(corpus_hash)
    compare_corpus_with_expected(
        expected_results["echidna"]["blacklisted_functions_seq"], new_corpus
    )


def test_echidna_function_filter_delete_sequence(
    setup_foundry_temp_dir: TempPathFactory,  # pylint: disable=unused-argument
) -> None:
    """Test that correct calls are deleted when filtering non-existent functions"""
    config = copy.deepcopy(default_config)
    config["corpusDir"] = "echidna-corpora/corpus-basic-modifier"
    config["targetContract"] = "BasicTypesNoCheckUint256"
    config["filterFunctions"] = True
    config["mode"] = "delete_sequence"
    config["fuzzer"] = "echidna"

    slither = Slither(config["compilationPath"])
    modifier = CorpusModifier(config, slither)

    new_corpus, corpus_hash = modifier.modify_corpus()

    modifier.restore_corpus_from_history(corpus_hash)
    compare_corpus_with_expected(expected_results["echidna"]["invalid_functions_seq"], new_corpus)


def test_echidna_modify_senders(
    setup_foundry_temp_dir: TempPathFactory,  # pylint: disable=unused-argument
) -> None:
    """Test that correct calls are modified when modifying senders"""
    config = copy.deepcopy(default_config)
    config["corpusDir"] = "echidna-corpora/corpus-basic-modifier"
    config["mode"] = "delete_calls"
    config["fuzzer"] = "echidna"
    config["modifySenders"] = {
        "0x0000000000000000000000000000000000010000": "0x0000000000000000000000000000000000020000"
    }

    modifier = CorpusModifier(config, None)
    new_corpus, corpus_hash = modifier.modify_corpus()

    modifier.restore_corpus_from_history(corpus_hash)
    compare_corpus_with_expected(expected_results["echidna"]["modify_senders"], new_corpus)


def test_medusa_delay_delete_calls(
    setup_foundry_temp_dir: TempPathFactory,
) -> None:
    """Test that correct calls are deleted when filtering by time and block delay"""
    config = copy.deepcopy(default_config)
    config["mode"] = "delete_calls"
    config["corpusDir"] = "medusa-corpora/corpus-basic-modifier"
    config["fuzzerConfigPath"] = "medusa.json"
    config["fuzzer"] = "medusa"

    create_file(
        setup_foundry_temp_dir,
        "medusa.json",
        '{"fuzzing": {"blockNumberDelayMax": 100,\n"blockTimestampDelayMax": 100}}',
    )

    modifier = CorpusModifier(config, None)
    new_corpus, corpus_hash = modifier.modify_corpus()

    modifier.restore_corpus_from_history(corpus_hash)
    compare_corpus_with_expected(expected_results["medusa"]["time_and_block_call"], new_corpus)


def test_medusa_function_filter_delete_calls(
    setup_foundry_temp_dir: TempPathFactory,  # pylint: disable=unused-argument
) -> None:
    """Test that correct calls are deleted when filtering non-existent functions"""
    config = copy.deepcopy(default_config)
    config["corpusDir"] = "medusa-corpora/corpus-basic-modifier"
    config["targetContract"] = "BasicTypesNoCheckUint256"
    config["filterFunctions"] = True
    config["mode"] = "delete_calls"
    config["fuzzer"] = "medusa"

    slither = Slither(config["compilationPath"])
    modifier = CorpusModifier(config, slither)

    new_corpus, corpus_hash = modifier.modify_corpus()
    modifier.restore_corpus_from_history(corpus_hash)
    compare_corpus_with_expected(expected_results["medusa"]["invalid_functions_call"], new_corpus)


def test_medusa_delay_delete_sequence(
    setup_foundry_temp_dir: TempPathFactory,
) -> None:
    """Test that correct calls are deleted when filtering by time and block delay"""
    config = copy.deepcopy(default_config)
    config["mode"] = "delete_sequence"
    config["corpusDir"] = "medusa-corpora/corpus-basic-modifier"
    config["fuzzerConfigPath"] = "medusa.json"
    config["fuzzer"] = "medusa"

    create_file(
        setup_foundry_temp_dir,
        "medusa.json",
        '{"fuzzing": {"blockNumberDelayMax": 100,\n"blockTimestampDelayMax": 100}}',
    )

    modifier = CorpusModifier(config, None)
    new_corpus, corpus_hash = modifier.modify_corpus()

    modifier.restore_corpus_from_history(corpus_hash)
    compare_corpus_with_expected(expected_results["medusa"]["time_and_block_seq"], new_corpus)


def test_medusa_function_filter_delete_sequence(
    setup_foundry_temp_dir: TempPathFactory,  # pylint: disable=unused-argument
) -> None:
    """Test that correct calls are deleted when filtering non-existent functions"""
    config = copy.deepcopy(default_config)
    config["corpusDir"] = "medusa-corpora/corpus-basic-modifier"
    config["targetContract"] = "BasicTypesNoCheckUint256"
    config["filterFunctions"] = True
    config["mode"] = "delete_sequence"
    config["fuzzer"] = "medusa"

    slither = Slither(config["compilationPath"])
    modifier = CorpusModifier(config, slither)

    new_corpus, corpus_hash = modifier.modify_corpus()
    modifier.restore_corpus_from_history(corpus_hash)
    compare_corpus_with_expected(expected_results["medusa"]["invalid_functions_seq"], new_corpus)


def test_medusa_modify_senders(
    setup_foundry_temp_dir: TempPathFactory,  # pylint: disable=unused-argument
) -> None:
    """Test that correct calls are modified when modifying senders"""
    config = copy.deepcopy(default_config)
    config["corpusDir"] = "medusa-corpora/corpus-basic-modifier"
    config["mode"] = "delete_calls"
    config["fuzzer"] = "medusa"
    config["modifySenders"] = {
        "0x0000000000000000000000000000000000010000": "0x0000000000000000000000000000000000020000"
    }

    modifier = CorpusModifier(config, None)
    new_corpus, corpus_hash = modifier.modify_corpus()
    modifier.restore_corpus_from_history(corpus_hash)
    compare_corpus_with_expected(expected_results["medusa"]["modify_senders"], new_corpus)
