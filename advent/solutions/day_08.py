import sys
import os
from pathlib import Path

# add root dir of project to sys path, to ensure relative imports work
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
script_path = Path(SCRIPT_DIR)
src_dir = script_path.parent.parent.absolute()
sys.path.insert(0, str(src_dir))


import math
import itertools
import re
from advent.common import (
    INPUTS_FOLDER,
    TEST_INPUTS_FOLDER,
    read_file_to_list_of_stripped_lines
)

INPUT_FILE_NAME = "8.txt"
INPUT_FILE_NAME_PART_TWO = "8_2.txt"
INPUT_FILE_PATH = Path(INPUTS_FOLDER, INPUT_FILE_NAME)
TEST_INPUT_FILE_PATH = Path(TEST_INPUTS_FOLDER, INPUT_FILE_NAME)
TEST_INPUT_PART_TWO_FILE_PATH = Path(TEST_INPUTS_FOLDER, INPUT_FILE_NAME_PART_TWO)

MapDictType = dict[str, tuple[str, str]]


def parse_input_part_one(input_file_path: str | Path = INPUT_FILE_PATH) -> tuple[str, MapDictType]:
    """
    Parse the puzzle input into a string containing the LR directions,
    and a dict representing the node map.

    Assumptions:
    - first line contains directions
    - second line is empty
    - subsequent lines contain the map
    """
    input_lines = read_file_to_list_of_stripped_lines(input_file_path)
    directions = input_lines[0]
    map = {}
    for index in range(2, len(input_lines)):
        line = input_lines[index]
        coordinates = re.findall(r'\b[A-Z]+\b', line)
        map[coordinates[0]] = (coordinates[1], coordinates[2])

    return directions, map


def find_destination_part_one(input_file_path: str | Path = INPUT_FILE_PATH) -> int:
    directions, map = parse_input_part_one(input_file_path)
    coordinate = "AAA"
    infinite_iterator = itertools.cycle(directions)
    count = 0
    for direction in infinite_iterator:
        next_coordinates = map[coordinate]
        if direction == "L":
            coordinate = next_coordinates[0]
        elif direction == "R":
            coordinate = next_coordinates[1]
        else:
            raise ValueError()
        count += 1
        if coordinate == "ZZZ":
            print(f"It took {count} steps to reach ZZZ")
            return count


def parse_input_part_two(input_file_path: str | Path = INPUT_FILE_PATH) -> tuple[str, list[str], MapDictType]:
    input_lines = read_file_to_list_of_stripped_lines(input_file_path)
    directions = input_lines[0]
    map = {}
    starting_coordinates = []
    for index in range(2, len(input_lines)):
        line = input_lines[index]
        coordinates = re.findall(r'\b[A-Z0-9]+\b', line)
        map[coordinates[0]] = (coordinates[1], coordinates[2])
        if coordinates[0][-1] == "A":
            starting_coordinates.append(coordinates[0])

    return directions, starting_coordinates, map


def find_destination_part_two_dumb(input_file_path: str | Path = INPUT_FILE_PATH) -> int:
    directions, starting_coordinates, map = parse_input_part_two(input_file_path)
    infinite_iterator = itertools.cycle(directions)
    current_coordinates = starting_coordinates
    count = 0
    for direction in infinite_iterator:
        next_coordinates = []
        for coordinate in current_coordinates:
            possible_next_coordinates = map[coordinate]
            if direction == "L":
                next_coordinate = possible_next_coordinates[0]
            elif direction == "R":
                next_coordinate = possible_next_coordinates[1]
            else:
                raise ValueError()
            next_coordinates.append(next_coordinate)
        count += 1
        all_end_in_Z = True
        for coordinate in next_coordinates:
            if coordinate[-1] != "Z":
                all_end_in_Z = False
        if all_end_in_Z:
            print(f"It took {count} steps to reach ZZZ")
            return count
        current_coordinates = next_coordinates


def find_destination_part_two_smart(input_file_path: str | Path = INPUT_FILE_PATH) -> int:
    directions, starting_coordinates, map = parse_input_part_two(input_file_path)
    infinite_iterator = itertools.cycle(directions)
    current_coordinates = starting_coordinates
    print(f"Starting coordinates: {starting_coordinates}")
    print(f"length: {len(current_coordinates)}")
    count = 1
    counts = []
    for direction in infinite_iterator:
        if not current_coordinates:
            break
        next_coordinates = []
        for coordinate in current_coordinates:
            possible_next_coordinates = map[coordinate]
            if direction == "L":
                next_coordinate = possible_next_coordinates[0]
            elif direction == "R":
                next_coordinate = possible_next_coordinates[1]
            else:
                raise ValueError()      
            if next_coordinate[-1] == "Z":
                counts.append(count)
            else:
                next_coordinates.append(next_coordinate)
        current_coordinates = next_coordinates
        count += 1
    print(f"counts: {counts}")
    print(f"length: {len(counts)}")
    answer = math.lcm(*counts)
    print(f"lowest common multiple: {answer}")
    return answer
    


if __name__ == "__main__":
    find_destination_part_two_smart()