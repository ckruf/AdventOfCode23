import sys
import os
from pathlib import Path

# add root dir of project to sys path, to ensure relative imports work
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
script_path = Path(SCRIPT_DIR)
src_dir = script_path.parent.parent.absolute()
sys.path.insert(0, str(src_dir))


import re
from advent.common import yield_lines, INPUTS_FOLDER

INPUT_FILE_NAME = "4.txt"
INPUT_FILE_PATH = Path(INPUTS_FOLDER, INPUT_FILE_NAME)


def count_duplicate_numbers(scratchcard: str) -> int:
    """Count how many numbers occur twice in the given sting"""
    count = 0
    numbers_start = scratchcard.find(":")
    numbers = re.findall(r'\d+', scratchcard[numbers_start + 1:])
    numbers.sort()
    for i in range(len(numbers) - 1):
        if numbers[i] == numbers[i + 1]:
            count += 1
    return count

def main_part_one(input_file_path: str | Path = INPUT_FILE_PATH):
    total = 0
    for scratchard in yield_lines(input_file_path):
        winning_number_count = count_duplicate_numbers(scratchard)
        if winning_number_count > 0:
            total += 2 ** (winning_number_count - 1)
    print(f"Total points from scratch cards: {total}")
    return total


if __name__ == "__main__":
    main_part_one()