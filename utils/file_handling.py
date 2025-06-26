from pathlib import Path
from shutil import copytree

def copy_directory(src, dst):
    copytree(src, dst, dirs_exist_ok=True)

def read_file(path):
    return Path(path).read_text()
