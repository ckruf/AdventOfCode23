"""
My main challenge with today's puzzle was that I wanted to achieve
the given tasks with a single iteration over the given string, only looking
at each character once.
"""
import sys
import os
from pathlib import Path

# add root dir of project to sys path, to ensure relative imports work
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
script_path = Path(SCRIPT_DIR)
src_dir = script_path.parent.parent.absolute()
print("src_dir", src_dir)
sys.path.insert(0, str(src_dir))


import time
from typing import NamedTuple, Optional
from advent.common import yield_lines, INPUTS_FOLDER

INPUT_FILE_NAME = "2.txt"
INPUT_FILE_PATH = Path(INPUTS_FOLDER, INPUT_FILE_NAME)


def find_number_beginning(input: str, index: int) -> int:
    """
    Given a string, and an index at which a (possibly multi-digit) 
    number ends, return the index where it starts
    """
    while input[index - 1].isdigit():
        index -= 1
    return index


def find_number_end(input: str, index: int) -> int:
    """
    Given a string, and an index at which a (possibly multi digit) number 
    starts, return the index at which it ends.
    """
    while input[index].isdigit():
        index += 1
    return index


class ExtractColorResult(NamedTuple):
    has_game_ended: bool
    has_hand_ended: bool
    ending_index: int


def find_color_end(game_input: str, index: int) -> ExtractColorResult:
    """
    Find the index of the next separator, which is where the color name ends.
    Also, provide information about whether the hand/game has ended, based
    on the separator.
    """
    while True:
        current_char = game_input[index]
        if current_char == ",":
            return ExtractColorResult(False, False, index)
        elif current_char == ";":
            return ExtractColorResult(False, True, index)
        elif current_char == "\n":
            return ExtractColorResult(True, True, index)
        elif index == len(game_input) - 1:
            return ExtractColorResult(True, True, index + 1)
        index += 1


def is_game_possible(
    game_input: str,
    red_max: int,
    green_max: int,
    blue_max: int
) -> int:
    """
    Given a game record string in the below format, and the maximum number of cubes of 
    each color, determine whether the game is possible. If it is, return
    the game id, if it isn't, return 0.

    Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green

    The function relies on the separators used.
    """
    game_id = None
    index = 0
    has_game_ended = False
    while index < len(game_input):
        if game_input[index] == ":":
            game_id_beginning = find_number_beginning(game_input, index - 1)
            game_id = int(game_input[game_id_beginning:index])
            index += 1
            break
        index += 1
    while not has_game_ended:
        has_game_ended, hand_possible, hand_end = is_hand_possible(game_input, index, red_max, green_max, blue_max)
        if not hand_possible:
            return 0
        index = hand_end + 1
            
    return game_id


class HandResult(NamedTuple):
    has_game_ended: bool
    is_hand_possible: bool
    ending_index: int


def is_hand_possible(
    game_input: str,
    start_index: int,
    red_max: int,
    green_max: int,
    blue_max: int 
) -> HandResult:
    """
    Given the whole game input string, and the index at which the the current
    hand starts, as well as the maxima of the different cubes, return whether
    the given hand is possible, and the index at which the current hand ends
    in the string.

    Return is_current_game, is_current_hand_possible, end_index
    """
    index = start_index
    current_number = None
    current_color = None
    is_hand_possible = True
    has_hand_ended = False
    has_game_ended = False

    while not has_hand_ended:
        if game_input[index].isdigit():
            number_end = find_number_end(game_input, index)
            current_number = int(game_input[index:number_end + 1])
            index = number_end
            continue
        elif game_input[index] == " ":
            index += 1
            continue 
        else:
            has_game_ended, has_hand_ended, color_end = find_color_end(game_input, index)
            current_color = game_input[index:color_end]
            index = color_end + 2  # skip over separator and space

        if current_color == "red":
            if current_number > red_max:
                is_hand_possible = False
        elif current_color == "green":
            if current_number > green_max:
                is_hand_possible = False
        elif current_color == "blue":
            if current_number > blue_max:
                is_hand_possible = False

    return HandResult(has_game_ended, is_hand_possible, color_end)

def main_part_one() -> None:
    total = 0
    for line in yield_lines(INPUT_FILE_PATH):
        total += is_game_possible(line, 12, 13, 14)
    print(f"The total is {total}")


class HandResults(NamedTuple):
    red_cubes: int
    green_cubes: int
    blue_cubes: int
    ending_index: int
    has_game_ended: bool


def cubes_in_hand(game_input: str, start_index: int) -> HandResults:
    index = start_index
    current_number: Optional[int] = None
    current_color: Optional[str] = None
    has_hand_ended = False
    has_game_ended = False
    red_cube_count = 0
    green_cube_count = 0
    blue_cube_count = 0

    while not has_hand_ended:
        if game_input[index].isdigit():
            number_end = find_number_end(game_input, index)
            current_number = int(game_input[index:number_end + 1])
            index = number_end
            continue
        elif game_input[index] == " ":
            index += 1
            continue 
        else:
            has_game_ended, has_hand_ended, color_end = find_color_end(game_input, index)
            current_color = game_input[index:color_end]
            index = color_end + 2  # skip over separator and space

        if current_color == "red":
            red_cube_count = current_number
        elif current_color == "green":
            green_cube_count = current_number
        elif current_color == "blue":
            blue_cube_count = current_number

    return HandResults(
        red_cube_count,
        green_cube_count,
        blue_cube_count,
        index,
        has_game_ended
    )


def cube_power_set(game_input: str) -> int:
    has_game_ended = False
    index = game_input.find(":") + 1
    max_red_count = 0
    max_green_count = 0
    max_blue_count = 0
    while not has_game_ended:
        hand_results = cubes_in_hand(game_input, index)
        index = hand_results.ending_index
        has_game_ended = hand_results.has_game_ended
        if hand_results.red_cubes > max_red_count:
            max_red_count = hand_results.red_cubes
        if hand_results.green_cubes > max_green_count:
            max_green_count = hand_results.green_cubes
        if hand_results.blue_cubes > max_blue_count:
            max_blue_count = hand_results.blue_cubes
            
    return max_red_count * max_green_count * max_blue_count


def main_part_two() -> None:
    total = 0
    for line in yield_lines(INPUT_FILE_PATH):
        power_set = cube_power_set(line)
        total += power_set
    print(f"The total is {total}")



if __name__ == "__main__":
    main_part_two()
