import os
from pathlib import Path
from typing import Generator


current_dir = Path(os.path.realpath(__file__)).parent
INPUTS_FOLDER = Path(current_dir, "inputs")
TEST_INPUTS_FOLDER = Path(current_dir, "tests", "inputs")


def yield_lines(file_path: str | Path) -> Generator[str, None, None]:
    """
    Generator yielding file at given file_path line by line.

    :param file_path: path of file which to read
    """
    with open(file_path, "r") as reader:
        for line in reader:
            yield line


def read_file(file_path: str | Path) -> str:
    """
    Read file all at once and return as string

    :param file_path: path of file which to read
    :return: entire file contents as str
    """
    with open(file_path, "r") as file:
        contents = file.read()
        return contents