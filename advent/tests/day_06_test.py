import sys
import os
from pathlib import Path

# add root dir of project to sys path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
script_path = Path(SCRIPT_DIR)

src_dir = script_path.parent.parent.absolute()
sys.path.insert(0, str(src_dir))
print(src_dir)


import pytest
from advent.common import TEST_INPUTS_FOLDER

TEST_INPUT_FILE_NAME = "6.txt"
TEST_INPUT_FILE_PATH = Path(TEST_INPUTS_FOLDER, TEST_INPUT_FILE_NAME)

from advent.solutions.day_06 import (
    main_part_one,
    solve_quadratic,
    compute_time_range_length,
    parse_input_part_one,
    parse_input_part_two,
    main_part_two
)


def test_solve_quadratic():
    first_solution, second_solution = solve_quadratic(-1, 7, -9)
    assert 1.69 < first_solution < 1.7
    assert 5.29 < second_solution < 5.31


@pytest.mark.parametrize(
    "distance, total_time, range_length",
    [
        (9, 7, 4),
        (40, 15, 8),
        (200, 30, 9)
    ]
)
def test_compute_time_range_length(distance, total_time ,range_length):
    assert compute_time_range_length(total_time, distance) == range_length


def test_main_part_one():
    assert main_part_one(TEST_INPUT_FILE_PATH) == 288

def test_parse_input_part_one():
    result = (
        [7, 15, 30],
        [9, 40, 200]
    )
    assert parse_input_part_one(TEST_INPUT_FILE_PATH) == result


def test_parse_input_part_two():
    assert parse_input_part_two(TEST_INPUT_FILE_PATH) == (71530, 940200)

def test_main_part_two():
    assert main_part_two(TEST_INPUT_FILE_PATH) == 71503