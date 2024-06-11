"""The CorpusModifier class handles modification of corpus call sequences based on fuzzer config"""
import os
import yaml
import hashlib
import json
import shutil
import copy
import datetime
from slither import Slither
from fuzz_utils.utils.error_handler import handle_exit

class CorpusModifier:
    """
    Handles modifying the corpus based on the fuzzer configuration.
    """
    fuzzer_fields: dict
    corpora_format: dict = {"echidna": {"coverage": [], "reproducers": []}, "medusa": {"call_sequences": {"immutable": [], "mutable": []}, "test_results": []}}

    def __init__(
        self,
        config_path: str | None,
        corpus_path: str | None,
        slither: Slither | None,
        fuzzer: str | None,
    ) -> None:
        self.fuzzer_fields = {}
        if slither:
            self.slither = slither
        if corpus_path:
            self.corpus_path = corpus_path
        if fuzzer:
            self.fuzzer = fuzzer
            self.fuzzer_fields["echidna"] = ["maxTimeDelay", "maxBlockDelay", "filterFunctions"]
        if config_path:
            self.config_path = config_path
            self.fuzzer_config = self._fetch_fuzzer_config(self.fuzzer_fields[fuzzer])
        self.corpus_copy = {}
    
    def modify_corpus(self) -> None:
        """Modifies the current corpus and saves the new version"""
        # 1. Open the corpus and parse all the files
        self.corpus_copy = self._copy_fuzzer_corpus(self.corpora_format[self.fuzzer.lower()], self.corpus_path)
        # 2. a) Copy current corpus somewhere in case something goes wrong?
        self.save_corpus_to_history()
        # 3. Define list of rules to apply
        # TODO update this later to be dynamic
        rules_list = [self._is_incorrect_delay]
        # 4. Apply the rules
        self._filter_corpus("filters_calls", rules_list)
        # 5. Save the new corpus
        self._override_corpus_directory(self.corpus_path, self.corpus_copy)

    def save_corpus_to_history(self) -> None:
        """Saves the current corpus directory to the corpus history"""
        # 1. Fetch current corpus
        corpus_to_save = self._copy_fuzzer_corpus(self.corpora_format[self.fuzzer.lower()], self.corpus_path)
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
        history[corpus_hash] = {"path": self.corpus_path, "timestamp": timestamp, "content": corpus_to_save, "comment": comment}
        # 7. Save history
        # TODO check if this can fail
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(history, f)
    
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
                print("No historic corpora were found.")



    def _override_corpus_directory(self, directory_path: str, contents_list: list) -> None:
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
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(file_content, file, indent=4)

    def _create_or_fetch_hidden_directory(self) -> str:
        current_directory = os.getcwd()
        directory_name = os.path.join(current_directory, ".fuzz_utils")
        os.makedirs(directory_name, exist_ok=True)
        return directory_name



    # TODO only supports Echidna for now
    def _is_incorrect_delay(self, call_object: dict) -> bool:
        maxTimeDelay = self.fuzzer_config["maxTimeDelay"] if "maxTimeDelay" in self.fuzzer_config else None
        maxBlockDelay = self.fuzzer_config["maxBlockDelay"] if "maxBlockDelay" in self.fuzzer_config else None

        if maxTimeDelay:
            time_delay = int(call_object["delay"][0], 16)
            if time_delay > maxTimeDelay:
                return True
        if maxBlockDelay:
            block_delay = int(call_object["delay"][1], 16)
            if block_delay > maxBlockDelay:
                return True

        return False

    def _filter_corpus(self, mode: str, rules_list: list) -> None:
        for idx, value in enumerate(self.corpus_copy):
            sequence_list: list = []
            # A list of files with call sequences in them
            for call_sequence in value["content"]:
                resulting_sequence = self._filter_call_sequence(mode, rules_list, call_sequence)

                if resulting_sequence:
                    sequence_list.append(resulting_sequence)

            # Override the old call sequences with the new ones
            self.corpus_copy[idx] = {"path": self.corpus_copy[idx]["path"], "content": sequence_list}

    def _filter_call_sequence(self, mode: str, rules_list: list, call_sequence: list) -> dict | None:
        def should_skip(call):
            return any(rule_fn(call) for rule_fn in rules_list)

        if mode not in {"delete_sequence", "filter_calls"}:
            raise ValueError("Invalid mode")

        resulting_sequence: dict = {"name": call_sequence["name"], "content": []}

        for call in call_sequence["content"]:
            if should_skip(call):
                if mode == "delete_sequence":
                    return None
            else:
                resulting_sequence["content"].append(call)

        return resulting_sequence if resulting_sequence["content"] else None


    def _copy_fuzzer_corpus(self, corpus: dict, current_path: str) -> list | None:
        temp_corpus = []
        for key in corpus.keys():
            subdir_path = os.path.join(current_path, key)
            if isinstance(corpus[key], dict):
                temp_corpus[key] = self._copy_fuzzer_corpus(corpus[key], subdir_path)
            else:
                temp_corpus.extend(self._fetch_directory_files(subdir_path))

        return temp_corpus if temp_corpus else None

    def _fetch_directory_files(self, directory: str) -> list:
        file_list: list = []
        if os.path.exists(directory):
            for entry in os.listdir(directory):
                full_path = os.path.join(directory, entry)

                if os.path.isfile(full_path):
                    try:
                        with open(full_path, "r", encoding="utf-8") as file:
                            if self.fuzzer.lower() == "echidna":
                                file_list.append({"path": full_path, "content": yaml.safe_load(file)})
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
                    if self.fuzzer.lower() == "echidna":
                        complete_config = yaml.safe_load(file)
                    else:
                        complete_config = json.load(file)
            except Exception: # pylint: disable=broad-except
                handle_exit(f"Failed to find the fuzzer configuration file at {self.config_path}")

        for key, value in complete_config.items():
            # TODO won't work for Medusa
            if key in fields:
                filtered_config[key] = value

        return filtered_config
        
