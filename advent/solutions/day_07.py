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

INPUT_FILE_NAME = "6.txt"
INPUT_FILE_PATH = Path(INPUTS_FOLDER, INPUT_FILE_NAME)
TEST_INPUT_FILE_PATH = Path(TEST_INPUTS_FOLDER, INPUT_FILE_NAME)


class HandStrength(Enum):
    FIVE_OF_A_KIND = 1
    FOUR_OF_A_KIND = 2
    FULL_HOUSE = 3
    THREE_OF_A_KIND = 4
    TWO_PAIR = 5
    ONE_PAIR = 6
    HIGH_CARD = 7


card_strength_order = ("2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A")

CardStrengths = {
    card_strength_order[i]: i for i in range(len(card_strength_order))
}


@dataclass(slots=True)
class Hand:
    cards: str
    strength: HandStrength

    def __init__(
        self,
        cards: str
    ):
        self.cards = cards
        symbol_counts = {}
        for symbol in cards:
            symbol_counts[symbol] = symbol_counts.get(symbol, 0) + 1
        ordered_counts = list(sorted(symbol_counts.values()))
        strength = self.determine_hand_type(ordered_counts)
        self.strength = strength

    @staticmethod
    def determine_hand_type(
        ordered_counts: list[int]
    ) -> HandStrength:
        
        if len(ordered_counts) == 1:
            return HandStrength.FIVE_OF_A_KIND
        elif len(ordered_counts) == 2:
            if ordered_counts[0] == 1:
                return HandStrength.FOUR_OF_A_KIND
            elif ordered_counts[1] == 2:
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
                strength_self = CardStrengths[symbol_self]
                strength_other = CardStrengths[symbol_other]
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
                strength_self = CardStrengths[symbol_self]
                strength_other = CardStrengths[symbol_other]
                return strength_self > strength_other
        else:
            return self.strength.value > other.strength.value