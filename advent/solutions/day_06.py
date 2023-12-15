import sys
import os
from pathlib import Path

# add root dir of project to sys path, to ensure relative imports work
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
script_path = Path(SCRIPT_DIR)
src_dir = script_path.parent.parent.absolute()
sys.path.insert(0, str(src_dir))


import math
import re
from typing import Union
from advent.common import (
    INPUTS_FOLDER,
    TEST_INPUTS_FOLDER,
    read_file_to_list_of_lines,
    extract_numbers,
    extract_to_single_number
)

INPUT_FILE_NAME = "6.txt"
INPUT_FILE_PATH = Path(INPUTS_FOLDER, INPUT_FILE_NAME)
TEST_INPUT_FILE_PATH = Path(TEST_INPUTS_FOLDER, INPUT_FILE_NAME)


QuadraticSolution = Union[None, float, tuple[float, float]]


def solve_quadratic(a: float, b: float, c: float) -> QuadraticSolution:
    """
    Solve a quadratic equation using the quadratic formula. Expects a, b, c;
    as in the form ax^2 + bx + c.

    No real solution: return None
    One real solution: return single float
    Two real solutions: return two float tuple
    """
    discriminant = math.pow(b, 2) - 4 * a * c
    if discriminant < 0:
        return None
    first_solution = (-b + math.sqrt(discriminant)) / (2 * a)
    if discriminant == 0:
        return first_solution
    second_solution = (-b - math.sqrt(discriminant)) / (2 * a)
    return first_solution, second_solution


def compute_time_range_length(total_time: int, distance: int) -> int:
    """
    Given the total available time, and the distance record that needs
    to be beaten, compute the size of the range of times which would
    exceed the given record.

    For example, consider a time of 7ms and a distance record of 9mm.
    This record can be beaten by holding the button for 2, 3, 4, or 5 milimetres.
    Therefore, the size of the range is 4 (contains 4 numbers). 
    """
    quadratic_solution = solve_quadratic(
        a=-1,
        b=total_time,
        c=-distance
    )
    if quadratic_solution is None:
        return 0
    if isinstance(quadratic_solution, float):
        return 1
    first_solution, second_solution = quadratic_solution
    if first_solution < second_solution:
        lower_bound = first_solution
        upper_bound = second_solution
    else:
        lower_bound = second_solution
        upper_bound = first_solution
    
    range_start = math.ceil(lower_bound)
    # in case where solution is like 10.0, we want to round to 11
    if range_start == lower_bound:
        range_start += 1
    range_end = math.floor(upper_bound)
    if range_end == upper_bound:
        range_end -= 1
    return range_end - range_start + 1


def parse_input_part_one(file_input_path: str | Path) -> tuple[list[int], list[int]]:
    puzzle_input = read_file_to_list_of_lines(file_input_path)
    times_line = puzzle_input[0]
    assert times_line.startswith("Time:")
    distances_line = puzzle_input[1]
    assert distances_line.startswith("Distance:")
    times = extract_numbers(times_line)
    distances = extract_numbers(distances_line)
    assert len(times) == len(distances)
    return times, distances


def main_part_one(file_input_path: str | Path = INPUT_FILE_PATH) -> int:
    times, distances = parse_input_part_one(file_input_path)
    total = 1
    for i in range(len(times)):
        combinations = compute_time_range_length(times[i], distances[i])
        total *= combinations
    print(f"The total number of ways is {total}")
    return total


def parse_input_part_two(file_input_path: str | Path) -> tuple[int, int]:
    puzzle_input = read_file_to_list_of_lines(file_input_path)
    times_line = puzzle_input[0]
    assert times_line.startswith("Time:")
    distances_line = puzzle_input[1]
    assert distances_line.startswith("Distance:")
    time = extract_to_single_number(times_line)
    distance = extract_to_single_number(distances_line)
    return time, distance


def main_part_two(file_input_path: str | Path = INPUT_FILE_PATH) -> int:
    time, distance = parse_input_part_two(file_input_path)
    total = compute_time_range_length(time, distance)
    print(f"The total number of ways is {total}")
    return total

if __name__ == "__main__":
    main_part_two()
