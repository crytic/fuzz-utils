"""The CorpusModifier class handles modification of corpus call sequences based on fuzzer config"""
import os
import hashlib
import json
import datetime
from collections import defaultdict
from typing import List, Dict, Union, Callable, Tuple

import yaml

from slither import Slither
from fuzz_utils.utils.slither_utils import get_target_contract
from fuzz_utils.utils.error_handler import handle_exit
from fuzz_utils.utils.crytic_print import CryticPrint
from fuzz_utils.modify_corpus.utils import (
    override_corpus_directory,
    create_or_fetch_hidden_directory,
    save_history,
    load_history,
)

# pylint: disable=too-many-instance-attributes
class CorpusModifier:
    """
    Handles modifying the corpus based on the fuzzer configuration.
    """

    fuzzer_fields: Dict[str, Dict[str, str]] = {
        "echidna": {
            "maxTimeDelay": "max_time_delay",
            "maxBlockDelay": "max_block_delay",
            "filterFunctions": "filter_functions",
        },
        "medusa": {
            "blockTimestampDelayMax": "max_time_delay",
            "blockNumberDelayMax": "max_block_delay",
        },
    }
    corpora_format: Dict[str, Dict[str, Union[List, Dict]]] = {
        "echidna": {"coverage": [], "reproducers": []},
        "medusa": {"call_sequences": {"immutable": [], "mutable": []}, "test_results": []},
    }
    valid_modes: List[str] = ["delete_sequence", "delete_calls"]
    fuzzer_config: Union[Dict, None] = None

    def __init__(self, config: Dict, slither: Union[Slither, None]) -> None:
        self.modifier_config = config
        self.slither = slither
        self.corpus_path = config.get("corpusDir", "")
        self.fuzzer = config.get("fuzzer", "")
        self.config_path = config.get("fuzzerConfigPath", "")
        self.mode = config.get("mode", "")
        if self.slither:
            self.target = (
                get_target_contract(self.slither, config["targetContract"])
                if "targetContract" in config
                else None
            )
        if self.config_path:
            self.fuzzer_config = self._fetch_fuzzer_config(self.fuzzer_fields.get(self.fuzzer, {}))
        self.corpus_copy: List[Dict] = []

        self.rules_list: List[Callable[[Dict], bool]] = [
            self._is_incorrect_delay,
            self._is_blacklisted_function,
            self._is_nonexistent_function,
        ]
        self.modifications_list: List[Callable[[Dict], Dict]] = [self._modify_invalid_caller]

    def modify_corpus(self) -> Tuple[List, str]:
        """Modifies the current corpus and saves the new version"""
        self.corpus_copy = self._copy_fuzzer_corpus(
            self.corpora_format[self.fuzzer], self.corpus_path
        )
        corpus_hash = self.save_corpus_to_history()
        new_corpus = self._filter_corpus(self.mode, self.rules_list, self.modifications_list)
        override_corpus_directory(self.corpus_path, new_corpus)
        return new_corpus, corpus_hash

    def dry_run(self) -> None:
        """Prints the calls that would be modified, without modifying them"""
        self.corpus_copy = self._copy_fuzzer_corpus(
            self.corpora_format[self.fuzzer], self.corpus_path
        )
        _ = self._filter_corpus(self.mode, self.rules_list, self.modifications_list)

    def save_corpus_to_history(self) -> str:
        """Saves the current corpus directory to the corpus history"""
        corpus_to_save = self._copy_fuzzer_corpus(
            self.corpora_format[self.fuzzer.lower()], self.corpus_path
        )
        directory = create_or_fetch_hidden_directory()
        corpus_str = json.dumps(corpus_to_save, sort_keys=True)
        corpus_hash = hashlib.sha256(corpus_str.encode()).hexdigest()
        history_path = os.path.join(directory, "history.json")

        history = load_history(history_path)
        if corpus_hash in history:
            print(f"The corpus is already saved to history with the hash {corpus_hash}")
            return corpus_hash

        timestamp = datetime.datetime.now().isoformat()
        comment = "test"  # input("Enter a comment for this save: ")
        history[corpus_hash] = {
            "path": self.corpus_path,
            "timestamp": timestamp,
            "content": corpus_to_save,
            "comment": comment,
        }
        save_history(history_path, history)
        CryticPrint().print_information(f"Corpus saved to history with hash: {corpus_hash}")
        return corpus_hash

    def restore_corpus_from_history(self, corpus_hash: str) -> None:  # pylint: disable=no-self-use
        """Overrides the current corpus directory with a historical version"""
        directory = create_or_fetch_hidden_directory()
        history_path = os.path.join(directory, "history.json")
        history = load_history(history_path)

        if corpus_hash in history:
            fetched_corpus = history[corpus_hash]
            override_corpus_directory(fetched_corpus["path"], fetched_corpus["content"])
        else:
            handle_exit("The provided hash was not found.")

    def list_historic_corpora(self) -> None:  # pylint: disable=no-self-use
        """Prints all the saved corpora"""
        directory = create_or_fetch_hidden_directory()
        history_path = os.path.join(directory, "history.json")
        history = load_history(history_path)

        if history:
            print("History:\n")
            for key, value in history.items():
                print(f'{key}: {value["comment"]} (saved at {value["timestamp"]})')
        else:
            print("No historic corpora found.")

    def _is_incorrect_delay(self, call_object: dict) -> bool:
        if not self.fuzzer_config:
            return False

        max_time_delay = self.fuzzer_config.get("max_time_delay")
        max_block_delay = self.fuzzer_config.get("max_block_delay")
        time_delay = (
            int(call_object["delay"][0], 16)
            if self.fuzzer == "echidna"
            else call_object["blockTimestampDelay"]
        )
        block_delay = (
            int(call_object["delay"][1], 16)
            if self.fuzzer == "echidna"
            else call_object["blockNumberDelay"]
        )

        if (max_time_delay and time_delay > max_time_delay) or (
            max_block_delay and block_delay > max_block_delay
        ):
            return True
        return False

    def _is_nonexistent_function(self, call_object: dict) -> bool:
        if "filterFunctions" not in self.modifier_config:
            return False

        function_name = (
            call_object["call"]["contents"][0]
            if self.fuzzer == "echidna"
            else call_object["call"]["dataAbiValues"]["methodSignature"].split("(")[0]
        )
        functions = [x.name for x in self.target.functions_entry_points]

        return function_name not in functions

    def _is_blacklisted_function(self, call_object: dict) -> bool:
        if not self.fuzzer_config or self.fuzzer == "medusa":
            return False

        function_name = call_object["call"]["contents"][0]
        blacklisted_functions = self.fuzzer_config.get("filter_functions", [])

        return function_name in blacklisted_functions if blacklisted_functions else False

    def _modify_invalid_caller(self, call_object: dict) -> dict:
        if "modifySenders" not in self.modifier_config:
            return call_object

        caller = call_object["src"] if self.fuzzer == "echidna" else call_object["call"]["from"]
        modified_caller = self.modifier_config["modifySenders"].get(caller)
        if modified_caller:
            if self.fuzzer == "echidna":
                call_object["src"] = modified_caller
            else:
                call_object["call"]["from"] = modified_caller
        return call_object

    def _filter_corpus(self, mode: str, rules_list: list, modification_list: list) -> list:
        if mode not in self.valid_modes:
            raise ValueError("Invalid mode")

        new_corpus: List[Dict] = []
        for value in self.corpus_copy:
            resulting_sequence = self._filter_call_sequence(
                mode, rules_list, modification_list, value["content"]
            )
            if resulting_sequence:
                new_corpus.append({"path": value["path"], "content": resulting_sequence})
        return new_corpus

    def _filter_call_sequence(
        self, mode: str, rules_list: list, modification_list: list, call_sequence: list
    ) -> list | None:
        def should_skip(call: Dict) -> bool:
            return any(rule_fn(call) for rule_fn in rules_list)

        def replace_fields(call: Dict) -> Dict:
            for modify_fn in modification_list:
                call = modify_fn(call)
            return call

        def replace_nonce(call: Dict, nonces: Dict) -> Dict:
            if self.fuzzer == "medusa":
                caller = call["call"]["from"]
                call["call"]["nonce"] = nonces[caller]
                nonces[caller] += 1

            return call

        nonces: dict = defaultdict(int)
        if self.fuzzer == "medusa":
            for call in call_sequence:
                if call["call"]["from"] not in nonces:
                    nonces[call["call"]["from"]] = call["call"]["nonce"]

        resulting_sequence: List = []
        for call in call_sequence:
            if should_skip(call):
                if mode == "delete_sequence":
                    return None
            else:
                # Modify call based on modifier rules, if applicable
                call = replace_fields(call)
                # Only used for Medusa#
                call = replace_nonce(call, nonces)
                # Append the call to the sequence
                resulting_sequence.append(call)

        return resulting_sequence if resulting_sequence else None

    def _copy_fuzzer_corpus(self, corpus: dict, current_path: str) -> list:
        temp_corpus: list = []

        for key, value in corpus.items():
            subdir_path = os.path.join(current_path, key)
            if isinstance(value, dict):
                print(value)
                temp_corpus.extend(self._copy_fuzzer_corpus(value, subdir_path))
            else:
                temp_corpus.extend(self._fetch_directory_files(subdir_path))

        return temp_corpus

    def _fetch_directory_files(self, directory: str) -> list:
        file_list: list = []
        if os.path.exists(directory):
            for entry in os.listdir(directory):
                full_path = os.path.join(directory, entry)

                if os.path.isfile(full_path):
                    try:
                        with open(full_path, "r", encoding="utf-8") as file:
                            if self.fuzzer == "echidna":
                                file_list.append(
                                    {"path": full_path, "content": yaml.safe_load(file)}
                                )
                            else:
                                file_list.append({"path": full_path, "content": json.load(file)})
                    except (yaml.YAMLError, json.JSONDecodeError, OSError) as e:
                        handle_exit(f"Failed to read file {full_path}: {e}")
        else:
            print(f"The provided corpus path does not exists: {directory}. Skipping.")

        return file_list

    def _fetch_fuzzer_config(self, fields: Dict) -> Dict:
        filtered_config = {}
        complete_config = {}
        if os.path.isfile(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as file:
                    complete_config = (
                        yaml.safe_load(file)
                        if self.fuzzer == "echidna"
                        else json.load(file)["fuzzing"]
                    )
            except (yaml.YAMLError, json.JSONDecodeError, OSError) as e:
                handle_exit(
                    f"Failed to find the fuzzer configuration file at {self.config_path}: {e}"
                )

        for key, value in complete_config.items():
            if key in fields:
                filtered_config[fields.get(key)] = value

        return filtered_config
