""" Utilities for managing corpus files"""
import os
import json
from typing import Dict
from fuzz_utils.utils.file_manager import clear_directory, write_directory_contents_json


def override_corpus_directory(directory_path: str, contents_list: list) -> None:
    """Cleares directory contents and then writes new ones"""
    clear_directory(directory_path)
    write_directory_contents_json(contents_list)


def create_or_fetch_hidden_directory() -> str:
    """Creates or fetched the .fuzz_utils directory"""
    directory_name = os.path.join(os.getcwd(), ".fuzz_utils")
    os.makedirs(directory_name, exist_ok=True)
    return directory_name


def save_history(history_path: str, history: Dict) -> None:
    """Save history to history.json"""
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history, f)


def load_history(history_path: str) -> Dict:
    """Load history.json from file"""
    if not os.path.exists(history_path):
        return {}
    with open(history_path, "r", encoding="utf-8") as f:
        return json.load(f)
