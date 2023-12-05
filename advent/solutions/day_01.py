import sys
import os
from pathlib import Path

# add root dir of project to sys path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
script_path = Path(SCRIPT_DIR)
src_dir = script_path.parent.parent.absolute()
print("src_dir", src_dir)
sys.path.insert(0, str(src_dir))


import re
import time
from typing import Optional
from advent.common import yield_lines, INPUTS_FOLDER

INPUT_FILE_NAME = "1.txt"
INPUT_FILE_PATH = Path(INPUTS_FOLDER, INPUT_FILE_NAME)

def extract_number(amended_calibration: str) -> int:
    """
    Extract the calibration value from the input string, by combining 
    the first digit and the last digit to form a single two-digit number.
    """
    first_digit: Optional[str] = None
    for char in amended_calibration:
        if char.isdigit():
            first_digit = char
            break
    second_digit: Optional[str] = None
    for char in reversed(amended_calibration):
        if char.isdigit():
            second_digit = char
            break
    number = first_digit + second_digit
    return int(number)

def extract_number_spelled(amended_calibration: str) -> int:
    """
    Extract the calibration value from the input string. Same principle as 
    above, except that digits can now also be spelled out ('one', 'two'..'nine')
    """
    number_mapping = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9
    }
    first_digit_index: Optional[int] = None
    last_digit_index: Optional[int] = None
    for i in range(len(amended_calibration)):
        if amended_calibration[i].isdigit():
            first_digit_index = i
            break
    if first_digit_index is not None:
        for i in range(len(amended_calibration) - 1, -1, -1):
            if amended_calibration[i].isdigit():
                last_digit_index = i
                break
    substring_indices = {
        "one": None,
        "two": None,
        "three": None,
        "four": None,
        "five": None,
        "six": None,
        "seven": None,
        "eight": None,
        "nine": None
    }
    for written_number in substring_indices:
        indices = [i.start() for i in re.finditer(written_number, amended_calibration)]
        substring_indices[written_number] = indices
    first_number = None
    lowest_index = len(amended_calibration)
    last_number = None
    highest_index = -1
    if first_digit_index is not None:
        lowest_index = first_digit_index
        first_number = int(amended_calibration[first_digit_index])
    if last_digit_index is not None:
        highest_index = last_digit_index
        last_number = int(amended_calibration[last_digit_index])
    for written_number, indices in substring_indices.items():
        if len(indices) > 0:
            minimum = min(indices)
            maximum = max(indices)
            if minimum < lowest_index:
                lowest_index = minimum
                first_number = number_mapping[written_number]
            if maximum > highest_index:
                highest_index = maximum
                last_number = number_mapping[written_number]
    return (10 * first_number) + last_number


def main_part_one() -> None:
    total = 0
    for line in yield_lines(INPUT_FILE_PATH):
        calibration = extract_number(line)
        total += calibration
    print(f"The total is {total}")


def main_part_two() -> None:
    start_time = time.perf_counter()
    total = 0
    for line in yield_lines(INPUT_FILE_PATH):
        calibration = extract_number_spelled(line)
        total += calibration
    end_time = time.perf_counter()
    print(f"The total is {total}")
    elapsed_time = (end_time - start_time) * 1_000
    print(f"The function took {elapsed_time} ms to run")


if __name__ == "__main__":
    main_part_two()
    