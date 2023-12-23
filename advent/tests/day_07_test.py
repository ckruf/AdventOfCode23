import sys
import os
from pathlib import Path

# add root dir of project to sys path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
script_path = Path(SCRIPT_DIR)

src_dir = script_path.parent.parent.absolute()
sys.path.insert(0, str(src_dir))
print(src_dir)


import pytest
from advent.common import TEST_INPUTS_FOLDER

TEST_INPUT_FILE_NAME = "7.txt"
TEST_INPUT_FILE_PATH = Path(TEST_INPUTS_FOLDER, TEST_INPUT_FILE_NAME)

from advent.solutions.day_07 import (
    Hand,
    HandStrength,
    main_part_one,
    JokerHand,
    main_part_two
)


@pytest.mark.parametrize(
    "input_line, hand_object",
    [
        ("32T3K 765", Hand("32T3K", 765)),
        ("T55J5 684", Hand("T55J5", 684)),
        ("KK677 28", Hand("KK677", 28))
    ]
)
def test_from_input_line(input_line, hand_object):
    assert Hand.from_input_line(input_line) == hand_object



@pytest.mark.parametrize(
    "hand_object, hand_strength",
    [
        (Hand("32T3K", 765), HandStrength.ONE_PAIR),
        (Hand("T55J5", 684), HandStrength.THREE_OF_A_KIND),
        (Hand("KK677", 28), HandStrength.TWO_PAIR),
        (Hand("KTJJT", 220), HandStrength.TWO_PAIR),
        (Hand("QQQJA", 483), HandStrength.THREE_OF_A_KIND),
        (Hand("A777A", 777), HandStrength.FULL_HOUSE),
        (Hand("AA7AA", 777), HandStrength.FOUR_OF_A_KIND)
    ]
)
def test_strength_categorization(hand_object, hand_strength):
    assert hand_object.strength == hand_strength


@pytest.mark.parametrize(
    "hand_object, hand_strength",
    [
        (JokerHand("32T3K", 765), HandStrength.ONE_PAIR),
        (JokerHand("T55J5", 684), HandStrength.FOUR_OF_A_KIND),
        (JokerHand("KK677", 28), HandStrength.TWO_PAIR),
        (JokerHand("KTJJT", 220), HandStrength.FOUR_OF_A_KIND),
        (JokerHand("QQQJA", 483), HandStrength.FOUR_OF_A_KIND),
    ]
)
def test_joker_strength_categorization(hand_object, hand_strength):
    assert hand_object.strength == hand_strength


@pytest.mark.parametrize(
    "smaller_hand, greater_hand",
    [
        (Hand("32T3K", 765), Hand("KTJJT", 220)),  # one pair vs two pair
        (Hand("A777A", 777), Hand("AA7AA", 777)),  # four of a kind vs full house
        (Hand("KTJJT", 220), Hand("QQQJA", 483)),  # three of a kind vs two pair
        (Hand("27772", 777), Hand("33222", 333)),  # full house vs full house 
        (Hand("32T3K", 765), Hand("41234", 765)),  # one pair vs one pair
    ]
)
def test_hand_comparison(smaller_hand, greater_hand):
    assert greater_hand > smaller_hand


def test_main_part_one():
    assert main_part_one(TEST_INPUT_FILE_PATH) == 6440


def test_main_part_two():
    assert main_part_two(TEST_INPUT_FILE_PATH) == 5905