"""
NOTE: this problem deals with ranges. ALL RANGES ARE REPRESENTED AS INCLUSIVE.
THERE IS NO OVERLAP BETWEEN RANGES.

So if we have f(x) = x + 2 act on, let' say, 50-97, and the next function
g(x) = x - 48 acts on a range of length two, immediately after the end of f(x)
range, then that would be represented as 98-99. The end of one range and 
the start of the next range ARE NEVER THE SAME NUMBER.
Ranges which immediately follow one another have a differene of 1.
"""
from __future__ import annotations

import sys
import os
from pathlib import Path

# add root dir of project to sys path, to ensure relative imports work
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
script_path = Path(SCRIPT_DIR)
src_dir = script_path.parent.parent.absolute()
sys.path.insert(0, str(src_dir))


from dataclasses import dataclass
import re
from advent.common import INPUTS_FOLDER, TEST_INPUTS_FOLDER, read_file_to_list_of_lines

INPUT_FILE_NAME = "5.txt"
INPUT_FILE_PATH = Path(INPUTS_FOLDER, INPUT_FILE_NAME)
TEST_INPUT_FILE_PATH = Path(TEST_INPUTS_FOLDER, INPUT_FILE_NAME)


@dataclass(slots=True)
class FunctionRange:
    """
    Class which represents a range, on which a linear function acts.
    For example, if the function f(x) = x-4 acts on the range 10-15, then
    this would be represented as FunctionRange(10, 15, -4). This would be
    a 'mapping range'. However, the class can also be used as an 'output range'.
    Continuing with the same example, the output range would be (14, 19, -4).
    Because when we apply the function f(x) = x-4 on the range 10-15, the 
    range of possible outputs is 14-19. The last argument remains the same.
    So it is context dependent - for a mapping range, the offset is the 
    offset that is going to be applied, and for an output range, the offset
    is the offset that has been applied. 
    """
    range_start: int
    range_end: int
    offset: int

    @classmethod
    def from_puzzle_input(
        cls,
        destination_range_start: int,
        source_range_start: int,
        range_length: int
    ):
        """
        Create a FunctionRange instance, representing a mapping range, from the
        AoC puzzle input.
        """
        range_start = source_range_start
        range_end = source_range_start + range_length - 1
        offset = destination_range_start - source_range_start
        return cls(range_start, range_end, offset)


@dataclass(slots=True)
class Mapper:
    input: str
    output: str
    mapping_ranges: list[FunctionRange]

    def map(self, source_value: int) -> int:
        for range in self.mapping_ranges:
            if range.range_start <= source_value <= range.range_end:
                return source_value + range.offset
        return source_value
    
    def compute_output_ranges(
            self,
            input_ranges: list[FunctionRange]
    ) -> list[FunctionRange]:
        """
        Given a list of input ranges, compute the possible output ranges
        obtained after the application of mapping functions.

        For example, if we have input ranges of 55-67 and 79-92, and 
        we have two mappings, f(x) = x + 2 in the range 50-97 and
        g(x) = x - 48 in the range 90-99, then the possible output ranges
        are 57-69 and and 81-94. 

        This is a simple example, because both input ranges are covered by 
        a single output range, but it can get much more complex.
        """
        output_ranges: list[FunctionRange] = []

        for input_range in input_ranges:
            input_sub_range_start = input_range.range_start

            for mapping_range in self.mapping_ranges:
                if (
                    mapping_range.range_start <= input_sub_range_start <= mapping_range.range_end  # input range start fits into function range
                    or mapping_range.range_start <= input_range.range_end <= mapping_range.range_end  # input range end fits into function range
                    or (input_sub_range_start <= mapping_range.range_start and input_range.range_end >= mapping_range.range_end)  # input range covers the function range entirely
                ):
                    if input_sub_range_start < mapping_range.range_start:
                        unmapped_range = FunctionRange(
                            input_sub_range_start,
                            mapping_range.range_start,
                            0
                        )
                        output_ranges.append(unmapped_range)

                    overlap_start = max(input_range.range_start, mapping_range.range_start)
                    overlap_end = min(input_range.range_end, mapping_range.range_end)

                    output_range_start = overlap_start + mapping_range.offset
                    output_range_end = overlap_end + mapping_range.offset
                    output_range = FunctionRange(
                        output_range_start,
                        output_range_end,
                        mapping_range.offset
                    )
                    output_ranges.append(output_range)
                    input_sub_range_start = overlap_end + 1
                    if input_sub_range_start >= input_range.range_end:
                        break

            if input_sub_range_start < input_range.range_end:
                unmapped_range = FunctionRange(
                    input_sub_range_start,
                    input_range.range_end,
                    0
                )
                output_ranges.append(unmapped_range)

        return output_ranges


def get_mapper_sequence(mappers_input: list[str]) -> list[Mapper]:
    """
    Given the puzzle text input, create a sequence of Mapper instances
    for each map provided in the file.

    Assumptions:
    - maps are titled with 'foo-to-bar map', where foo and bar can be string
    - maps are described using an arbitrary number of lines containing 3 numbers
    """
    mappers: list[Mapper] = []
    input_len = len(mappers_input)
    row_index = 0
    while row_index < input_len:
        # find whether current line contains map description, split with '-to-'
        map_input_and_output: list[tuple[str, str]] = re.findall(
            r"(\w+)-to-(\w+)",
            mappers_input[row_index]
        )
        if map_input_and_output and len(map_input_and_output[0]) == 2:
            # current line indeed contained map description, extract range
            # information from following lines 
            input, output = map_input_and_output[0]
            ranges: list[FunctionRange] = []
            row_index += 1
            numbers = re.findall(r"\b\d+\b", mappers_input[row_index])
            while len(numbers) == 3:
                range = FunctionRange.from_puzzle_input(int(numbers[0]), int(numbers[1]), int(numbers[2]))
                ranges.append(range)
                row_index += 1
                if row_index == input_len:
                    break
                numbers = re.findall(r"\b\d+\b", mappers_input[row_index])
            ranges.sort(key=lambda x: x.range_start)
            mappers.append(Mapper(input, output, ranges))
        else:
            row_index += 1
    return mappers


def apply_mappers(seed: int, mappers: list[Mapper]) -> int:
    """
    Given the number of the seed, and a list of all mappers, apply the
    'map' operation of each mapper to get to the location number.
    """
    transformed_value = seed
    for mapper in mappers:
        transformed_value = mapper.map(transformed_value)
    return transformed_value


def get_seeds(input_text: list[str]) -> list[int]:
    """
    Given the puzzle input, extract the seed numbers.
    Assumptions:
    - line starts with 'seeds:'
    """
    for line in input_text:
        if line.startswith("seeds:"):
            numbers = re.findall(r"\b\d+\b", line)
            return [int(number) for number in numbers]


def main_part_one(puzzle_input_file_path: str | Path = INPUT_FILE_PATH) -> int:
    puzzle_input = read_file_to_list_of_lines(puzzle_input_file_path)
    seeds = get_seeds(puzzle_input)
    mappers = get_mapper_sequence(puzzle_input)
    locations = [apply_mappers(seed, mappers) for seed in seeds]
    print("locations: ", locations)
    lowest_location = min(locations)
    print(f"The lowest location is {lowest_location}")
    return lowest_location


def get_seed_ranges(puzzle_input: list[str]) -> list[FunctionRange]:
    """
    Given the puzzle input, represent the possible seed values as 
    function range instances.
    """
    for line in puzzle_input:
        if line.startswith("seeds:"):
            stringified_numbers = re.findall(r"\b\d+\b", line)
            range_numbers = [int(number) for number in stringified_numbers]
    seed_ranges: list[FunctionRange] = []
    for i in range(0, len(range_numbers), 2):
        range_start = range_numbers[i]
        range_end = range_numbers[i] + range_numbers[i+1] - 1
        seed_range = FunctionRange(
            range_start,
            range_end,
            0
        )
        seed_ranges.append(seed_range)
    return seed_ranges


def brute_part_two(puzzle_input_file_path: str | Path = INPUT_FILE_PATH) -> None:
    """
    Brute force solution for part two
    """
    print("brute")
    puzzle_input = read_file_to_list_of_lines(puzzle_input_file_path)
    seed_data = get_seeds(puzzle_input)
    mappers = get_mapper_sequence(puzzle_input)
    seed_numbers: list[int] = []
    for i in range(0, len(seed_data), 2):
        seed_numbers.extend(j for j in range(seed_data[i], seed_data[i]+seed_data[i+1]))
    values = seed_numbers
    for mapper in mappers:
        values = [mapper.map(value) for value in values]
        print(f"for {mapper.input}-to-{mapper.output}, possible values are:")
        values.sort()
        print(values)
    print("\n")


def main_part_two(puzzle_input_file_path: str | Path = INPUT_FILE_PATH) -> int:
    """
    Smart solution for part two
    """
    puzzle_input = read_file_to_list_of_lines(puzzle_input_file_path)
    seed_ranges = get_seed_ranges(puzzle_input)
    seed_ranges.sort(key=lambda x: x.range_start)
    print(seed_ranges)
    mappers = get_mapper_sequence(puzzle_input)
    ranges = seed_ranges
    for mapper in mappers:
        ranges = mapper.compute_output_ranges(ranges)
        print(f"for {mapper.input}-to-{mapper.output}, possible ranges are:")
        ranges.sort(key=lambda x: x.range_start)
        print(ranges)
    min_value = ranges[0].range_start
    print("min value: ", min_value)
    return min_value


if __name__ == "__main__":
    brute_part_two(TEST_INPUT_FILE_PATH)
    main_part_two(TEST_INPUT_FILE_PATH)