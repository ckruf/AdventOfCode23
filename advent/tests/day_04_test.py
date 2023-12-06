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
    main_part_one
)


def test_main_part_one():
    print(TEST_INPUTS_FOLDER)
    print(TEST_INPUT_FILE_PATH)
    assert main_part_one(TEST_INPUT_FILE_PATH) == 13