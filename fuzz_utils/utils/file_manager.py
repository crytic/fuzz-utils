""" Manages creation of files and directories """
import os


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
