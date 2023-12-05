import sys
import os
from pathlib import Path

# add root dir of project to sys path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
script_path = Path(SCRIPT_DIR)
src_dir = script_path.parent.parent.absolute()
sys.path.insert(0, str(src_dir))

# from advent.solutions.day01 import extract__number
from advent.solutions.day_02 import find_number_beginning, find_color_end, ExtractColorResult, HandResult, is_hand_possible, is_game_possible, cube_power_set
import pytest


@pytest.mark.parametrize(
    "input_string, end_index, start_index",
    [
        ("Game 1: 3 blue, 4 red", 5, 5),
        ("Game 12: 3 blue, 4 red", 6, 5),
        ("Game 123: 3 blue, 4 red", 7, 5),
    ]
)
def test_find_number_beginning(input_string, end_index, start_index):
    assert find_number_beginning(input_string, end_index) == start_index


@pytest.mark.parametrize(
    "input_string, index, result",
    [
        ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\n", 8, ExtractColorResult(False, False, 14)),
        ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\n", 16, ExtractColorResult(False, True, 21)),
        ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\n", 47, ExtractColorResult(True, True, 54)),
    ]
)
def test_find_color_end(input_string, index, result):
    assert find_color_end(input_string, index) == result



@pytest.mark.parametrize(
    "game_input, start_index, red_max, green_max, blue_max, result",
    [
        ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\n", 8, 10, 10, 10, HandResult(False, True, 21)),
        ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\n", 23, 10, 10, 10, HandResult(False, True, 45)),
        ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\n", 23, 2, 2, 2, HandResult(False, False, 45)),
        ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\n", 47, 10, 10, 10, HandResult(True, True, 54)),
    ]
)
def test_is_hand_possible(
    game_input,
    start_index,
    red_max,
    green_max,
    blue_max,
    result
):
    assert is_hand_possible(game_input, start_index, red_max, green_max, blue_max) == result


@pytest.mark.parametrize(
    "game_input, red_max, green_max, blue_max, result",
    [
        ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\n", 12, 13, 14, 1),
        ("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue\n", 12, 13, 14, 2),
        ("Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red\n", 12, 13, 14, 0),
        ("Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red\n", 12, 13, 14, 0),
        ("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green\n", 12, 13, 14, 5),
    ]
)
def test_is_game_possible(game_input, red_max, green_max, blue_max, result):
    assert is_game_possible(game_input, red_max, green_max, blue_max) == result


@pytest.mark.parametrize(
    "game_input, result",
    [
        ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\n", 48),
        ("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue\n", 12),
        ("Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red\n", 1560),
        ("Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red\n", 630),
        ("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green\n", 36),
        ("Game 100: 8 green; 2 red, 20 green; 12 green, 1 red, 1 blue; 4 red, 1 blue; 1 blue, 6 red", 120)
    ]
)
def test_cube_power_set(game_input, result):
    assert cube_power_set(game_input) == result
