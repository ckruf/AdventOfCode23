import sys
import os
from pathlib import Path

# add root dir of project to sys path, to ensure relative imports work
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
script_path = Path(SCRIPT_DIR)
src_dir = script_path.parent.parent.absolute()
sys.path.insert(0, str(src_dir))


from dataclasses import dataclass
from enum import Enum
from typing import Union
from advent.common import (
    INPUTS_FOLDER,
    TEST_INPUTS_FOLDER,
    read_file_to_list_of_stripped_lines
)

INPUT_FILE_NAME = "7.txt"
INPUT_FILE_PATH = Path(INPUTS_FOLDER, INPUT_FILE_NAME)
TEST_INPUT_FILE_PATH = Path(TEST_INPUTS_FOLDER, INPUT_FILE_NAME)


class HandStrength(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7


@dataclass(slots=True)
class Hand:
    cards: str
    strength: HandStrength
    bid: int
    card_strength_order = ("2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A")
    card_strengths: dict[str, int]

    def __init__(
        self,
        cards: str,
        bid: int
    ):
        self.card_strengths = {
            self.card_strength_order[i]: i for i in range(len(self.card_strength_order))
        }
        self.cards = cards
        self.bid = bid
        symbol_counts: dict[str, int] = {}
        for symbol in cards:
            symbol_counts[symbol] = symbol_counts.get(symbol, 0) + 1
        ordered_counts = list(sorted(symbol_counts.values()))
        strength = self.determine_hand_type(ordered_counts)
        self.strength = strength

    @classmethod
    def from_input_line(cls, input_line: str):
        hand, bid = input_line.split()
        bid = int(bid)
        return cls(hand, bid)

    @staticmethod
    def determine_hand_type(
        ordered_counts: list[int]
    ) -> HandStrength:
        
        if len(ordered_counts) == 1:
            return HandStrength.FIVE_OF_A_KIND
        elif len(ordered_counts) == 2:
            if ordered_counts[0] == 1:
                return HandStrength.FOUR_OF_A_KIND
            elif ordered_counts[0] == 2:
                return HandStrength.FULL_HOUSE
            else:
                raise ValueError()
        elif len(ordered_counts) == 3:
            if ordered_counts[-1] == 3:
                return HandStrength.THREE_OF_A_KIND
            elif ordered_counts[-1] == 2:
                return HandStrength.TWO_PAIR
            else:
                raise ValueError()
        elif len(ordered_counts) == 4:
            assert ordered_counts[-1] == 2
            return HandStrength.ONE_PAIR
        else:
            return HandStrength.HIGH_CARD
        
    def __lt__(self, other) -> bool:
        assert type(self) is type(other)
        assert len(self.cards) == len(other.cards)
        if self.strength == other.strength:
            for i in range(len(self.cards)):
                if self.cards[i] == other.cards[i]:
                    continue
                symbol_self = self.cards[i]
                symbol_other = other.cards[i]
                strength_self = self.card_strengths[symbol_self]
                strength_other = self.card_strengths[symbol_other]
                return strength_self < strength_other

        else:
            return self.strength.value < other.strength.value
        
    def __gt__(self, other) -> bool:
        assert type(self) is type(other)
        if self.strength == other.strength:
            for i in range(len(self.cards)):
                if self.cards[i] == other.cards[i]:
                    continue
                symbol_self = self.cards[i]
                symbol_other = other.cards[i]
                strength_self = self.card_strengths[symbol_self]
                strength_other = self.card_strengths[symbol_other]
                return strength_self > strength_other
        else:
            return self.strength.value > other.strength.value


@dataclass(slots=True)
class JokerHand(Hand):

    card_strength_order = ("J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A")

    def __init__(
        self,
        cards: str,
        bid: int
    ):
        self.card_strengths = {
            self.card_strength_order[i]: i for i in range(len(self.card_strength_order))
        }
        self.cards = cards
        self.bid = bid
        symbol_counts = {}
        for symbol in cards:
            symbol_counts[symbol] = symbol_counts.get(symbol, 0) + 1
        ordered_counts = list(sorted(symbol_counts.values()))
        if "J" in symbol_counts:
            strength = self.determine_hand_type_joker(ordered_counts, symbol_counts)
        else:
            strength = self.determine_hand_type(ordered_counts)
        self.strength = strength

    @staticmethod
    def determine_hand_type_joker(
        ordered_counts: list[int],
        symbol_counts: dict[str, int]
    ) -> HandStrength:
        if len(ordered_counts) == 1:
            return HandStrength.FIVE_OF_A_KIND
        elif len(ordered_counts) == 2:
            return HandStrength.FIVE_OF_A_KIND
        elif len(ordered_counts) == 3:
            if ordered_counts[-1] == 3:
                return HandStrength.FOUR_OF_A_KIND
            elif ordered_counts[-1] == 2:
                if symbol_counts["J"] == 2:
                    return HandStrength.FOUR_OF_A_KIND
                return HandStrength.FULL_HOUSE
            else:
                raise ValueError()
        elif len(ordered_counts) == 4:
            assert ordered_counts[-1] == 2
            return HandStrength.THREE_OF_A_KIND
        else:
            return HandStrength.ONE_PAIR


def parse_to_list_of_hands(input_file_path: str | Path) -> list[Hand]:
    card_lines = read_file_to_list_of_stripped_lines(input_file_path)
    hands = map(lambda x: Hand.from_input_line(x), card_lines)
    return list(hands)


def parse_to_list_of_joker_hands(input_file_path: str | Path) -> list[JokerHand]:
    card_lines = read_file_to_list_of_stripped_lines(input_file_path)
    hands = map(lambda x: JokerHand.from_input_line(x), card_lines)
    return list(hands)


def compute_total_winnings(sorted_hands: list[Hand]) -> int:
    total = 0
    for index, hand in enumerate(sorted_hands):
        hand_winnings = (index + 1) * hand.bid
        total += hand_winnings
    return total


def main_part_one(input_file_path: str | Path = INPUT_FILE_PATH) -> int:
    hands = parse_to_list_of_hands(input_file_path)
    hands.sort()
    total_winnings = compute_total_winnings(hands)
    print(f"The total winnings are {total_winnings}")
    return total_winnings


def main_part_two(input_file_path: str | Path = INPUT_FILE_PATH) -> int:
    hands = parse_to_list_of_joker_hands(input_file_path)
    hands.sort()
    total_winnings = compute_total_winnings(hands)
    print(f"The total winnings are {total_winnings}")
    return total_winnings


if __name__ == "__main__":
    main_part_one()
    main_part_two()