""" Manages creation of files and directories """
import os
import json
import shutil
from typing import List, Dict


def clear_directory(directory_path: str) -> None:
    """Deletes directory including all the contents"""
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            os.remove(os.path.join(root, file))
        for directory in dirs:
            shutil.rmtree(os.path.join(root, directory))


def write_directory_contents_json(contents_list: List[Dict]) -> None:
    """
    Takes a list of dictionaries [{`path`: `path/to/file.ext`, `content`: ``}, ...] and
    writes all the files, creating directories along the way.
    """
    for item in contents_list:
        file_path = item["path"]
        file_content = item["content"]
        if file_content:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(file_content, file, indent=4)


def check_and_create_dirs(base_path: str, dirnames: list[str]) -> None:
    """Checks if the directories in the list exist, if not, creates them"""
    for dirname in dirnames:
        path = os.path.join(base_path, dirname)
        if not os.path.exists(path):
            os.makedirs(path)


def save_file(path: str, file_name: str, suffix: str, content: str) -> None:
    """Saves a file"""
    with open(f"{path}{file_name}{suffix}", "w", encoding="utf-8") as outfile:
        outfile.write(content)
