""" Manages creation of files and directories """
import os

def check_and_create_dir(dirname: str) -> None:
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    
def save_files(path: str, file_name: str, suffix: str, content: str) -> None:
    with open(f"{path}{file_name}{suffix}", "w", encoding="utf-8") as outfile:
        outfile.write(content)