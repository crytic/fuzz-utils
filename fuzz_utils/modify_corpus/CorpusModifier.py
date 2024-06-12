"""The CorpusModifier class handles modification of corpus call sequences based on fuzzer config"""
import os
import hashlib
import json
import shutil
import datetime
import yaml

from slither import Slither
from fuzz_utils.utils.slither_utils import get_target_contract
from fuzz_utils.utils.error_handler import handle_exit
from fuzz_utils.utils.crytic_print import CryticPrint

# pylint: disable=too-many-instance-attributes
class CorpusModifier:
    """
    Handles modifying the corpus based on the fuzzer configuration.
    """

    fuzzer_fields: dict = {
        "echidna": ["maxTimeDelay", "maxBlockDelay", "filterFunctions"],
        "medusa": ["blockTimestampDelayMax", "blockNumberDelayMax"],
    }
    corpora_format: dict = {
        "echidna": {"coverage": [], "reproducers": []},
        "medusa": {"call_sequences": {"immutable": [], "mutable": []}, "test_results": []},
    }
    valid_modes: list = ["delete_sequence", "delete_calls"]
    fuzzer_config: dict | None = None

    def __init__(self, config: dict, slither: Slither | None) -> None:
        if config:
            self.modifier_config = config
        if slither:
            self.slither = slither
        if "corpusDir" in config:
            self.corpus_path = config["corpusDir"]
        if "fuzzer" in config:
            self.fuzzer = config["fuzzer"]
        if "fuzzerConfigPath" in config:
            self.config_path = config["fuzzerConfigPath"]
            self.fuzzer_config = self._fetch_fuzzer_config(self.fuzzer_fields[self.fuzzer])
        if "mode" in config:
            self.mode = config["mode"]
        if "targetContract" in config:
            self.target = get_target_contract(self.slither, config["targetContract"])
        self.corpus_copy: list = []
        self.rules_list = [
            self._is_incorrect_delay,
            self._is_blacklisted_function,
            self._is_nonexistent_function,
        ]
        self.modifications_list = [self._modify_invalid_caller]

    def modify_corpus(self) -> None:
        """Modifies the current corpus and saves the new version"""
        # 1. Open the corpus and parse all the files
        self.corpus_copy = self._copy_fuzzer_corpus(
            self.corpora_format[self.fuzzer], self.corpus_path
        )
        # 2. a) Copy current corpus somewhere in case something goes wrong?
        self.save_corpus_to_history()
        # 4. Apply the rules
        new_corpus = self._filter_corpus(self.mode, self.rules_list, self.modifications_list)
        # 5. Save the new corpus
        self._override_corpus_directory(self.corpus_path, new_corpus)

    def dry_run(self) -> None:
        """Prints the calls that would be modified, without modifying them"""
        self.corpus_copy = self._copy_fuzzer_corpus(
            self.corpora_format[self.fuzzer.lower()], self.corpus_path
        )
        _ = self._filter_corpus(self.mode, self.rules_list, self.modifications_list)

    def save_corpus_to_history(self) -> None:
        """Saves the current corpus directory to the corpus history"""
        # 1. Fetch current corpus
        corpus_to_save = self._copy_fuzzer_corpus(
            self.corpora_format[self.fuzzer.lower()], self.corpus_path
        )
        # 2. Check if .fuzz_utils folder already exists, create it if not
        directory = self._create_or_fetch_hidden_directory()
        # 3. Convert into a string
        corpus_str = json.dumps(corpus_to_save, sort_keys=True)
        # 4. Hash it
        corpus_hash = hashlib.sha256(corpus_str.encode()).hexdigest()
        # 5. Check if hash already exists, skip operation and print a message if it does
        history: dict
        history_path = os.path.join(directory, "history.json")
        # TODO check if this can fail
        if not os.path.exists(history_path):
            with open(history_path, "w", encoding="utf-8") as f:
                f.write("{}")

        with open(history_path, "r", encoding="utf-8") as f:
            history = json.load(f)

        if corpus_hash in history.keys():
            print(f"The corpus is already saved to history with the hash {corpus_hash}")
            return
        # 6. Add to history
        timestamp = datetime.datetime.now().isoformat()
        comment = input("Enter a comment for this save: ")
        history[corpus_hash] = {
            "path": self.corpus_path,
            "timestamp": timestamp,
            "content": corpus_to_save,
            "comment": comment,
        }
        # 7. Save history
        # TODO check if this can fail
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(history, f)

        CryticPrint().print_information(f"Corpus saved to history with hash: {corpus_hash}")

    def restore_corpus_from_history(self, corpus_hash: str) -> None:
        """Overrides the current corpus directory with a historical version"""
        directory = self._create_or_fetch_hidden_directory()
        history_path = os.path.join(directory, "history.json")
        fetched_corpus: dict
        # TODO check if this can fail
        with open(history_path, "r", encoding="utf-8") as f:
            history = json.load(f)

            if corpus_hash in history.keys():
                fetched_corpus = history[corpus_hash]
                self._override_corpus_directory(fetched_corpus["path"], fetched_corpus["content"])
            else:
                handle_exit("The provided hash was not found.")

    def list_historic_corpora(self) -> None:
        """Prints all the saved corpora"""
        directory = self._create_or_fetch_hidden_directory()
        history_path = os.path.join(directory, "history.json")

        with open(history_path, "r", encoding="utf-8") as f:
            history = json.load(f)

            if history:
                print("History:\n")
                for key, value in history.items():
                    print(f'{key}: {value["comment"]} (saved at {value["timestamp"]})')
            else:
                print("No historic corpora found.")

    def _override_corpus_directory(  # pylint: disable=no-self-use
        self, directory_path: str, contents_list: list
    ) -> None:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
            for directory in dirs:
                dir_path = os.path.join(root, directory)
                shutil.rmtree(dir_path)

        for item in contents_list:
            file_path = item["path"]
            file_content = item["content"]

            if file_content:
                # Ensure the directory exists
                directory = os.path.dirname(file_path)
                os.makedirs(directory, exist_ok=True)

                # Write the file contents
                # TODO fix the mypy errors later on
                with open(file_path, "w", encoding="utf-8") as file:  # type: ignore[assignment]
                    json.dump(file_content, file, indent=4)  # type: ignore[arg-type]

    def _create_or_fetch_hidden_directory(self) -> str:  # pylint: disable=no-self-use
        current_directory = os.getcwd()
        directory_name = os.path.join(current_directory, ".fuzz_utils")
        os.makedirs(directory_name, exist_ok=True)
        return directory_name

    def _is_incorrect_delay(self, call_object: dict) -> bool:
        if not self.fuzzer_config:
            return False

        maxTimeDelay: int | None
        maxBlockDelay: int | None
        time_delay: int
        block_delay: int

        if self.fuzzer == "echidna":
            maxTimeDelay = (
                self.fuzzer_config["maxTimeDelay"] if "maxTimeDelay" in self.fuzzer_config else None
            )
            maxBlockDelay = (
                self.fuzzer_config["maxBlockDelay"]
                if "maxBlockDelay" in self.fuzzer_config
                else None
            )
            time_delay = int(call_object["delay"][0], 16)
            block_delay = int(call_object["delay"][1], 16)
        elif self.fuzzer == "medusa":
            maxTimeDelay = (
                self.fuzzer_config["fuzzing"]["blockTimestampDelayMax"]
                if "blockTimestampDelayMax" in self.fuzzer_config["fuzzing"]
                else None
            )
            maxBlockDelay = (
                self.fuzzer_config["fuzzing"]["blockNumberDelayMax"]
                if "blockNumberDelayMax" in self.fuzzer_config["fuzzing"]
                else None
            )
            time_delay = call_object["blockTimestampDelay"]
            block_delay = call_object["blockNumberDelay"]
        else:
            raise ValueError(f"Invalid fuzzer: {self.fuzzer}")

        if maxTimeDelay:
            if time_delay > maxTimeDelay:
                return True
        if maxBlockDelay:
            if block_delay > maxBlockDelay:
                return True

        return False

    def _is_nonexistent_function(self, call_object: dict) -> bool:
        if "filterFunctions" not in self.modifier_config:
            return False

        function_name: str
        # contracts = self.slither.contracts_derived
        # functions = [y.name for x in contracts for y in x.functions_entry_points]
        # TODO enable multiple targets later
        functions = [x.name for x in self.target.functions_entry_points]

        if self.fuzzer == "echidna":
            function_name = call_object["call"]["contents"][0]
        elif self.fuzzer == "medusa":
            function_name = call_object["call"]["dataAbiValues"]["methodSignature"].split("(")[0]
        else:
            raise ValueError(f"Invalid fuzzer: {self.fuzzer}")
        print(f"fnName {function_name}, functions list {functions}")
        if function_name not in functions:
            return True
        return False

    def _is_blacklisted_function(self, call_object: dict) -> bool:
        if not self.fuzzer_config:
            return False

        function_name: str
        blacklisted_functions: list | None
        if self.fuzzer == "echidna":
            function_name = call_object["call"]["contents"][0]
            blacklisted_functions = (
                self.fuzzer_config["filterFunctions"]
                if "filterFunctions" in self.fuzzer_config
                else None
            )
        else:
            raise ValueError("Function blacklisting is only available in Echidna.")

        if blacklisted_functions:
            if (
                function_name in blacklisted_functions
            ):  # pylint: disable=unsupported-membership-test
                return True
        return False

    def _modify_invalid_caller(self, call_object: dict) -> dict:
        if "modifySenders" not in self.modifier_config:
            return call_object

        print("modifySenders run")
        caller = call_object["src"]
        if caller in self.modifier_config["modifySenders"].keys():
            call_object["src"] = self.modifier_config["modifySenders"][caller]
        return call_object

    def _filter_corpus(self, mode: str, rules_list: list, modification_list: list) -> list:
        new_corpus: list = []
        for idx, value in enumerate(self.corpus_copy):
            # A list of files with call sequences in them
            resulting_sequence = self._filter_call_sequence(
                mode, rules_list, modification_list, value["content"]
            )

            if resulting_sequence:
                new_corpus.append(
                    {"path": self.corpus_copy[idx]["path"], "content": resulting_sequence}
                )
        return new_corpus

    def _filter_call_sequence(
        self, mode: str, rules_list: list, modification_list: list, call_sequence: list
    ) -> list | None:
        def should_skip(call: dict) -> bool:
            return any(rule_fn(call) for rule_fn in rules_list)

        def replace_fields(call: dict) -> dict:
            for modify_fn in modification_list:
                call = modify_fn(call)
            return call

        if mode not in self.valid_modes:
            raise ValueError("Invalid mode")

        resulting_sequence: list = []

        for call in call_sequence:
            # TODO make this remove calls
            if should_skip(call):
                if mode == "delete_sequence":
                    return None
            else:
                call = replace_fields(call)
                resulting_sequence.append(call)

        return resulting_sequence if resulting_sequence else None

    def _copy_fuzzer_corpus(self, corpus: dict, current_path: str) -> list:
        temp_corpus: list = []
        for key in corpus.keys():
            subdir_path = os.path.join(current_path, key)
            if isinstance(corpus[key], dict):
                temp_corpus[key] = self._copy_fuzzer_corpus(corpus[key], subdir_path)
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
                            if self.fuzzer.lower() == "echidna":
                                file_list.append(
                                    {"path": full_path, "content": yaml.safe_load(file)}
                                )
                            else:
                                file_list.append({"path": full_path, "content": json.load(file)})
                    except Exception:  # pylint: disable=broad-except
                        print(f"Fail on {full_path}")
        else:
            print(f"The provided corpus path does not exists: {directory}. Skipping.")

        return file_list

    def _fetch_fuzzer_config(self, fields: list[str]) -> dict:
        filtered_config: dict = {}
        complete_config: dict
        if os.path.isfile(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as file:
                    if self.fuzzer == "echidna":
                        complete_config = yaml.safe_load(file)
                    else:
                        complete_config = json.load(file)["fuzzing"]
            except Exception:  # pylint: disable=broad-except
                handle_exit(f"Failed to find the fuzzer configuration file at {self.config_path}")

        for key, value in complete_config.items():
            if key in fields:
                filtered_config[key] = value

        return filtered_config
