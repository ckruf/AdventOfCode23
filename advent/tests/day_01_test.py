import sys
import os
from pathlib import Path

# add root dir of project to sys path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
script_path = Path(SCRIPT_DIR)
src_dir = script_path.parent.parent.absolute()
sys.path.insert(0, str(src_dir))

# from advent.solutions.day01 import extract__number
from advent.solutions.day_01 import extract_number, extract_number_spelled
import pytest



@pytest.mark.parametrize(
    "input_string, extracted_number",
    [
        ("1abc2", 12),
        ("pqr3stu8vwx", 38),
        ("a1b2c3d4e5f", 15),
        ("treb7uchet", 77),
    ]
)
def test_extract_number(input_string, extracted_number):
    assert extract_number(input_string) == extracted_number


@pytest.mark.parametrize(
    "input_string, extracted_number",
    [
        ("two1nine", 29),
        ("eightwothree", 83),
        ("abcone2threexyz", 13),
        ("xtwone3four", 24),
        ("4nineeightseven2", 42),
        ("zoneight234", 14),
        ("7pqrstsixteen", 76)
    ]
)
def test_extract_number_spelled(input_string, extracted_number):
    assert extract_number_spelled(input_string) == extracted_number