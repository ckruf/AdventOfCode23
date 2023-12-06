import sys
import os
from pathlib import Path

# add root dir of project to sys path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
script_path = Path(SCRIPT_DIR)
src_dir = script_path.parent.parent.absolute()
sys.path.insert(0, str(src_dir))

import pytest
from advent.solutions.day_03 import (
    sum_engine_part_numbers,
    get_surrounding_indices,
    is_symbol_adjacent,
    get_surrounding_numbers,
    sum_gear_ratios
)

# test results for generate indices
# 467 from test str
results_top_left = [
    (1, 0),
    (1, 1),
    (1, 2),
    (0, 3),
    (1, 3),
]

# 114 from test str
results_top_row = [
    (1, 5),
    (1, 6),
    (1, 7),
    (0, 4),
    (0, 8),
    (1, 4),
    (1, 8),
]

# 35 from test str
results_third_row = [
    (1, 2),
    (1, 3),
    (3, 2),
    (3, 3),
    (2, 1),
    (2, 4),
    (1, 1),
    (1, 4),
    (3, 1),
    (3, 4)
]

# 664 from test str
results_last_row = [
    (8, 1),
    (8, 2),
    (8, 3),
    (9, 0),
    (9, 4),
    (8, 0),
    (8, 4)
]


@pytest.mark.parametrize(
    "row_index, row_count, line_length, number_start_index, number_end_index, answer",
    [
        (0, 10, 10, 0, 2, results_top_left),
        (0, 10, 10, 5, 7, results_top_row),
        (2, 10, 10, 2, 3, results_third_row),
        (9, 10, 10, 1, 3, results_last_row)
    ]
)
def test_get_surrounding_indices(
    row_index,
    row_count,
    line_length,
    number_start_index,
    number_end_index,
    answer
):
    result = get_surrounding_indices(
        row_index,
        row_count,
        line_length,
        number_start_index,
        number_end_index
    )
    assert result == answer

test_input = [
    '467..114..', 
    '...*......',
    '..35..633.',
    '......#...', 
    '617*......',
    '.....+.58.',
    '..592.....',
    '......755.',
    '...$.*....',
    '.664.598..'
]

test_input_2 = [
    '467.1.14..', 
    '...*......',
    '.35.4.633.',
    '......#...', 
    '617*......',
    '.....+.58.',
    '..592.....',
    '......755.',
    '...$.*....',
    '.664.598..'
]

@pytest.mark.parametrize(
    "schematic, row_index, number_start_index, number_end_index, answer",
    [
        (test_input, 0, 0, 2, True),
        (test_input, 0, 5, 7, False),
        (test_input, 2, 2, 3, True),
        (test_input, 9, 1, 3, True)
    ]
)
def test_is_symbol_adjacent(
    schematic,
    row_index,
    number_start_index,
    number_end_index,
    answer
):
    assert is_symbol_adjacent(
        schematic,
        row_index,
        number_start_index,
        number_end_index
    ) is answer


def test_sum_engine_part_numbers():
    assert sum_engine_part_numbers(test_input) == 4361


@pytest.mark.parametrize(
    "row_index, character_index, schematic, answer",
    [
        (1, 3, test_input, [467, 35]),
        (4, 3, test_input, [617,]),
        (8, 5, test_input, [755, 598]),
        (1, 3, test_input_2, [467, 1, 35, 4])
    ]
)
def test_get_surrounding_numbers(row_index, character_index, schematic, answer):
    result = get_surrounding_numbers(row_index, character_index, schematic)
    result.sort()
    answer.sort()
    assert result == answer


def test_sum_gear_ratios():
    assert sum_gear_ratios(test_input) == 467835