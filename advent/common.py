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
    

def read_file_to_list_of_lines(file_path: str | Path) -> str:
    """
    Read file all at once and return as a list of strings, where each element
    in the list corresponds to one line in the text file.
    """
    with open(file_path, "r") as file:
        lines = file.readlines()
        return lines
    

def read_file_to_list_of_stripped_lines(file_path: str | Path) -> str:
    """
    Read file all at once and return as a list of strings, where each element
    in the list corresponds to one line in the text file. Each line is stripped
    of trailing whitespace.
    """
    with open(file_path, "r") as file:
        lines = file.readlines()
        stripped_lines = [line.rstrip() for line in lines]
        return stripped_lines


def find_number_end(input: str, beginning_index: int) -> int:
    """
    Given a string, and an index at which a (possibly multi digit) number 
    starts, return the index at which it ends (meaning the first index 
    which does not form part of the number anymore - makes sense for slicing)
    """
    while beginning_index < len(input) and input[beginning_index].isdigit():
        beginning_index += 1
    return beginning_index


def find_number_beginning(input: str, end_index: int) -> int:
    """
    Given a string, and an index at which a (possibly multi-digit) 
    number ends, return the index where it starts (meaning the index of the 
    first digit - makes sense for slicing)
    """
    while input[end_index - 1].isdigit():
        end_index -= 1
    return end_index
