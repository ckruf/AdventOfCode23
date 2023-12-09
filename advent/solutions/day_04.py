import sys
import os
from pathlib import Path

# add root dir of project to sys path, to ensure relative imports work
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
script_path = Path(SCRIPT_DIR)
src_dir = script_path.parent.parent.absolute()
sys.path.insert(0, str(src_dir))


import re
from advent.common import yield_lines, INPUTS_FOLDER, TEST_INPUTS_FOLDER

INPUT_FILE_NAME = "4.txt"
INPUT_FILE_PATH = Path(INPUTS_FOLDER, INPUT_FILE_NAME)
TEST_INPUT_FILE_PATH = Path(TEST_INPUTS_FOLDER, INPUT_FILE_NAME)


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


def count_points_for_every_card(input_file_path: str | Path) -> dict[int, int]:
    points = {}
    for scratchcard in yield_lines(input_file_path):
        all_numbers = re.findall(r'\d+', scratchcard)
        card_id = int(all_numbers[0])
        duplicate_count = 0
        unique_numbers = set()
        for i in range(1, len(all_numbers)):
            if all_numbers[i] in unique_numbers:
                duplicate_count += 1
            else:
                unique_numbers.add(all_numbers[i])
        points[card_id] = duplicate_count
    return points


def count_all_cards(input_file_path: str | Path) -> int:
    all_card_points = count_points_for_every_card(input_file_path)
    total = 0
    all_cards = list(reversed(all_card_points.keys()))
    while all_cards:
        current_card = all_cards.pop()
        total += 1
        current_card_points = all_card_points[current_card]
        for i in range(current_card + 1, current_card_points + current_card + 1):
            all_cards.append(i)
    return total


if __name__ == "__main__":
    print(count_all_cards(INPUT_FILE_PATH))