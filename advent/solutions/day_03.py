import sys
import os
from pathlib import Path

# add root dir of project to sys path, to ensure relative imports work
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
script_path = Path(SCRIPT_DIR)
src_dir = script_path.parent.parent.absolute()
sys.path.insert(0, str(src_dir))


import time
from advent.common import read_file_to_list_of_stripped_lines, INPUTS_FOLDER, find_number_end, find_number_beginning

INPUT_FILE_NAME = "3.txt"
INPUT_FILE_PATH = Path(INPUTS_FOLDER, INPUT_FILE_NAME)


def sum_engine_part_numbers(schematic: list[str]) -> int:
    total = 0
    for i in range(len(schematic)):
        j = 0
        while j < len(schematic[i]):
            if schematic[i][j].isdigit():
                number_end_index = find_number_end(schematic[i], j)
                number = int(schematic[i][j:number_end_index])
                if is_symbol_adjacent(
                    schematic=schematic,
                    row_index=i,
                    number_start_index=j,
                    number_end_index=number_end_index - 1
                ):
                    total += number
                j = number_end_index
            else:
                j += 1
    return total


def is_symbol_adjacent(
    schematic: list[str],
    row_index: int,
    number_start_index: int,
    number_end_index: int
) -> bool:
    row_count = len(schematic)
    line = schematic[row_index]
    surrounding_indices = get_surrounding_indices(
        row_index=row_index,
        row_count=row_count,
        line_length=len(line),
        start_index=number_start_index,
        end_index=number_end_index
    )
    symbol_adjacent = False
    for row, col in surrounding_indices:
        char = schematic[row][col]
        if not char.isdigit() and char != ".":
            symbol_adjacent = True
    
    return symbol_adjacent


def get_surrounding_indices(
    row_index: int,
    row_count: int,
    line_length: int,
    start_index: int,
    end_index: int
) -> list[tuple[int, int]]:
    """
    Given the beginning index and end index of a substring in one of the rows 
    in a text file, generate a list of surrounding indices.

    :param row_index: index of the row that the substring is found in
    :param row_count: total number of rows in the text file
    :param line_length: length of the row that the substring is found in
    :param start_index: index of the beginning of the substring in the row
    :param end_index: index of the end of the substring in the row
    """
    surrounding_indices: list[tuple[int, int]] = []
    row_above = row_index > 0
    row_below = row_index < row_count - 1
    column_left = start_index > 0
    column_right = end_index < line_length - 1

    # get above and below indices
    if row_above:
        indices_above = [(row_index - 1, i) for i in range(start_index, end_index + 1)]
        surrounding_indices.extend(indices_above)
    if row_below:
        indices_below = [(row_index + 1, i) for i in range(start_index, end_index + 1)]
        surrounding_indices.extend(indices_below)
    # get left and right indices
    if column_left:
        index_left = row_index, start_index - 1
        surrounding_indices.append(index_left)
    if column_right:
        index_right = row_index, end_index + 1
        surrounding_indices.append(index_right)
    # get diagonal indices
    if row_above and column_left:
        top_left = row_index - 1, start_index - 1
        surrounding_indices.append(top_left)
    if row_above and column_right:
        top_right = row_index - 1, end_index + 1
        surrounding_indices.append(top_right)
    if row_below and column_left:
        bottom_left = row_index + 1, start_index - 1
        surrounding_indices.append(bottom_left)
    if row_below and column_right:
        bottom_right = row_index + 1, end_index + 1
        surrounding_indices.append(bottom_right)

    return surrounding_indices


def main_part_one() -> None:
    input = read_file_to_list_of_stripped_lines(INPUT_FILE_PATH)
    engine_parts_sum = sum_engine_part_numbers(input)
    print(f"The engine parts sum is {engine_parts_sum}")


def get_surrounding_numbers(
    row_index: int,
    character_index: int,
    schematic: list[str],
) -> list[int]:
    """
    Given the index of a character in one of the rows in a text file,
    generate a list of surrounding numbers in the text file.

    :param row_index: index of the row that the substring is found in
    :param row_count: total number of rows in the text file
    :param line_length: length of the row that the substring is found in
    :param character_index: index of the character in the row
    """
    row_count = len(schematic)
    line_length = len(schematic[row_index])
    surrounding_numbers: list[int] = []
    row_above = row_index > 0
    row_below = row_index < row_count - 1
    column_left = character_index > 0
    column_right = character_index < line_length - 1

    is_number_directly_above = False
    is_number_directly_below = False

    if row_above:
        character_above = schematic[row_index - 1][character_index]
        if character_above.isdigit():
            is_number_directly_above = True
            number_beginning = find_number_beginning(schematic[row_index - 1], character_index)
            number_end = find_number_end(schematic[row_index - 1], character_index)
            number = int(schematic[row_index - 1][number_beginning:number_end])
            surrounding_numbers.append(number)
    if row_below:
        character_below = schematic[row_index + 1][character_index]
        if character_below.isdigit():
            is_number_directly_below = True
            number_beginning = find_number_beginning(schematic[row_index + 1], character_index)
            number_end = find_number_end(schematic[row_index + 1], character_index)
            number = int(schematic[row_index + 1][number_beginning:number_end])
            surrounding_numbers.append(number)
    if column_left:
        character_left = schematic[row_index][character_index - 1]
        if character_left.isdigit():
            number_beginning = find_number_beginning(schematic[row_index], character_index - 1)
            number = int(schematic[row_index][number_beginning:character_index])
            surrounding_numbers.append(number)
    if column_right:
        character_right = schematic[row_index][character_index + 1]
        if character_right.isdigit():
            number_end = find_number_end(schematic[row_index], character_index + 1)
            number = int(schematic[row_index][character_index + 1:number_end])
            surrounding_numbers.append(number)

    if row_above and column_left and not is_number_directly_above:
        character_top_left = schematic[row_index - 1][character_index - 1]
        if character_top_left.isdigit():
            number_beginning = find_number_beginning(schematic[row_index - 1], character_index - 1)
            number = int(schematic[row_index - 1][number_beginning:character_index])
            surrounding_numbers.append(number)
    if row_above and column_right and not is_number_directly_above:
        character_top_right = schematic[row_index - 1][character_index + 1]
        if character_top_right.isdigit():
            number_end = find_number_end(schematic[row_index - 1], character_index + 1)
            number = int(schematic[row_index - 1][character_index + 1:number_end])
            surrounding_numbers.append(number)
    if row_below and column_left and not is_number_directly_below:
        character_bottom_left = schematic[row_index + 1][character_index - 1]
        if character_bottom_left.isdigit():
            number_beginning = find_number_beginning(schematic[row_index + 1], character_index - 1)
            number = int(schematic[row_index + 1][number_beginning:character_index])
            surrounding_numbers.append(number)
    if row_below and column_right and not is_number_directly_below:
        character_bottom_right = schematic[row_index + 1][character_index + 1]
        if character_bottom_right.isdigit():
            number_end = find_number_end(schematic[row_index + 1], character_index + 1)
            number = int(schematic[row_index + 1][character_index + 1:number_end])
            surrounding_numbers.append(number)

    return surrounding_numbers


def sum_gear_ratios(schematic: list[str]) -> int:
    total = 0
    for i in range(len(schematic)):
        for j in range(len(schematic[i])):
            if schematic[i][j] == "*":
                surrounding_numbers = get_surrounding_numbers(i, j, schematic)
                if len(surrounding_numbers) == 2:
                    gear_ratio = surrounding_numbers[0] * surrounding_numbers[1]
                    total += gear_ratio
    return total


def main_part_two() -> None:
    input = read_file_to_list_of_stripped_lines(INPUT_FILE_PATH)
    result = sum_gear_ratios(input)
    print(f"The sum of gear ratios is {result}")


if __name__ == "__main__":
    main_part_two()