import sys
import os
from pathlib import Path

# add root dir of project to sys path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
script_path = Path(SCRIPT_DIR)

src_dir = script_path.parent.parent.absolute()
sys.path.insert(0, str(src_dir))


import pytest
from advent.common import TEST_INPUTS_FOLDER

TEST_INPUT_FILE_NAME = "5.txt"
TEST_INPUT_FILE_PATH = Path(TEST_INPUTS_FOLDER, TEST_INPUT_FILE_NAME)

from advent.solutions.day_05 import (
    main_part_one,
    Mapper,
    FunctionRange,
    get_mapper_sequence
)


def test_main_part_one():
    lowest_location = main_part_one(TEST_INPUT_FILE_PATH)
    assert lowest_location == 35



class TestComputeOutputRanges:

    @staticmethod
    def test_fits_entirely_within_single_range():
        """
        Test the scenario where the input range fits entirely within
        a mapping range
        """
        mapping_range = FunctionRange(
            range_start=10,
            range_end=20,
            offset=3
        )
        input_range = FunctionRange(
            range_start=12,
            range_end=15,
            offset=5
        )
        mapper = Mapper(
            input="foo",
            output="bar",
            function_ranges=[mapping_range,]
        )
        output_ranges = mapper.compute_output_ranges([input_range,])
        assert len(output_ranges) == 1
        output_range = output_ranges[0]
        assert output_range == FunctionRange(
            range_start=15,
            range_end=18,
            offset=3
        )

    @staticmethod
    def test_spans_two_ranges():
        """
        Test scenario where the input range start is within one mapping range,
        and the input range end is within the following mapping range
        """
        first_mapping_range = FunctionRange(
            range_start=7,
            range_end=11,
            offset=50
        )
        second_mapping_range = FunctionRange(
            range_start=11,
            range_end=53,
            offset=-11
        )
        input_range = FunctionRange(
            range_start=9,
            range_end=25,
            offset=5
        )
        mapper = Mapper(
            input="foo",
            output="bar",
            function_ranges=[first_mapping_range, second_mapping_range]
        )
        output_ranges = mapper.compute_output_ranges([input_range,])
        assert len(output_ranges) == 2
        first_output_range = output_ranges[0]
        assert first_output_range == FunctionRange(
            range_start=59,
            range_end=61,
            offset=50
        )
        second_output_range = output_ranges[1]
        assert second_output_range == FunctionRange(
            range_start=0,
            range_end=14,
            offset=-11
        )


    @staticmethod
    def test_input_range_starts_before_any_mapping_range():
        """
        Test scenario where the input range starts before the start of 
        the first mapping range. In this case, that part of the input
        should go through unmapped (meaning 'mapped' through f(x)=x)
        """
        first_mapping_range = FunctionRange(
            range_start=7,
            range_end=11,
            offset=50
        )
        second_mapping_range = FunctionRange(
            range_start=11,
            range_end=53,
            offset=-11
        )
        input_range = FunctionRange(
            range_start=2,
            range_end=25,
            offset=5
        )
        mapper = Mapper(
            input="foo",
            output="bar",
            function_ranges=[first_mapping_range, second_mapping_range]
        )
        output_ranges = mapper.compute_output_ranges([input_range,])
        assert len(output_ranges) == 3

        first_output_range = output_ranges[0]
        assert first_output_range == FunctionRange(
            range_start=2,
            range_end=7,
            offset=0
        )
        second_output_range = output_ranges[1]
        assert second_output_range == FunctionRange(
            range_start=57,
            range_end=61,
            offset=50
        )
        third_output_range = output_ranges[2]
        assert third_output_range == FunctionRange(
            range_start=0,
            range_end=14,
            offset=-11
        )

    @staticmethod
    def test_input_range_ends_after_last_mapping_range():
        """
        Test scenario where the input range ends after the end of the 
        last mapping range. In this case, that last part of the input
        (the 'overhang') should go through unmapped (meaning 'mapped'
        through f(x)=x).
        """
        first_mapping_range = FunctionRange(
            range_start=7,
            range_end=11,
            offset=50
        )
        second_mapping_range = FunctionRange(
            range_start=11,
            range_end=53,
            offset=-11
        )
        input_range = FunctionRange(
            range_start=9,
            range_end=60,
            offset=5
        )
        mapper = Mapper(
            input="foo",
            output="bar",
            function_ranges=[first_mapping_range, second_mapping_range]
        )
        output_ranges = mapper.compute_output_ranges([input_range,])
        assert len(output_ranges) == 3
        first_output_range = output_ranges[0]
        assert first_output_range == FunctionRange(
            range_start=59,
            range_end=61,
            offset=50
        )
        second_output_range = output_ranges[1]
        assert second_output_range == FunctionRange(
            range_start=0,
            range_end=42,
            offset=-11
        )
        third_output_range = output_ranges[2]
        assert third_output_range == FunctionRange(
            range_start=53,
            range_end=60,
            offset=0
        )



def test_get_mapper_sequence():
    map_description = [
        "seed-to-soil map",
        "50 98 2",
        "52 50 48"
    ]
    mappers = get_mapper_sequence(map_description)
    assert len(mappers) == 1
    seed_to_soil_mapper = mappers[0]
    mapping_ranges = seed_to_soil_mapper.function_ranges
    assert len(mapping_ranges) == 2
    first_mapping_range = mapping_ranges[0]
    assert first_mapping_range == FunctionRange(
        range_start=50,
        range_end=97,
        offset=2
    )
    second_mapping_range = mapping_ranges[1]
    assert second_mapping_range == FunctionRange(
        range_start=98,
        range_end=99,
        offset=-48
    )



def test_get_mappers_and_compute_output_ranges():
    """
    
    """
    pass