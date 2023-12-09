import sys
import os
from pathlib import Path

# add root dir of project to sys path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
script_path = Path(SCRIPT_DIR)

src_dir = script_path.parent.parent.absolute()
sys.path.insert(0, str(src_dir))


import pytest
from advent.common import TEST_INPUTS_FOLDER

TEST_INPUT_FILE_NAME = "4.txt"
TEST_INPUT_FILE_PATH = Path(TEST_INPUTS_FOLDER, TEST_INPUT_FILE_NAME)

from advent.solutions.day_04 import (
    main_part_one,
    count_points_for_every_card,
    count_all_cards
)


def test_main_part_one():
    print(TEST_INPUTS_FOLDER)
    print(TEST_INPUT_FILE_PATH)
    assert main_part_one(TEST_INPUT_FILE_PATH) == 13


def test_count_points_for_every_card():
    result = count_points_for_every_card(TEST_INPUT_FILE_PATH)
    assert result == {
        1: 4,
        2: 2,
        3: 2,
        4: 1,
        5: 0,
        6: 0
    }


if __name__ == "__main__":
    print(count_all_cards(TEST_INPUT_FILE_PATH))