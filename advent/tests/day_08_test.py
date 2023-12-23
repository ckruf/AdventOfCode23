import sys
import os
from pathlib import Path

# add root dir of project to sys path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
script_path = Path(SCRIPT_DIR)

src_dir = script_path.parent.parent.absolute()
sys.path.insert(0, str(src_dir))
print(src_dir)


from advent.common import TEST_INPUTS_FOLDER

TEST_INPUT_FILE_NAME = "8.txt"
TEST_INPUT_PART_TWO_FILE_NAME = "8_2.txt"
TEST_INPUT_FILE_PATH = Path(TEST_INPUTS_FOLDER, TEST_INPUT_FILE_NAME)
TEST_INPUT_PART_TWO_FILE_PATH = Path(TEST_INPUTS_FOLDER, TEST_INPUT_PART_TWO_FILE_NAME)

from advent.solutions.day_08 import (
    parse_input_part_one,
    find_destination_part_one,
    parse_input_part_two,
    find_destination_part_two_dumb,
    find_destination_part_two_smart
)



def test_parse_input_part_one():
    directions, map = parse_input_part_one(TEST_INPUT_FILE_PATH)
    assert directions == "LLR"
    assert map == {
        "AAA": ("BBB", "BBB"),
        "BBB": ("AAA", "ZZZ"),
        "ZZZ": ("ZZZ", "ZZZ")
    }


def test_find_destination_part_one():
    assert find_destination_part_one(TEST_INPUT_FILE_PATH) == 6


def test_parse_input_part_two():
    directions, starting_coordinates, map = parse_input_part_two(TEST_INPUT_PART_TWO_FILE_PATH)
    assert starting_coordinates == ["11A", "22A"]


def test_find_destination_part_two():
    assert find_destination_part_two_dumb(TEST_INPUT_PART_TWO_FILE_PATH) == 6


def test_find_destination_part_two_smart():
    assert find_destination_part_two_smart(TEST_INPUT_PART_TWO_FILE_PATH) == 6