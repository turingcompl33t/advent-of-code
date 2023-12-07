"""
part1.py

Advent of Code 2023, Day 7, Part 1.
"""

from __future__ import annotations

import sys
import argparse
from collections import defaultdict
from pathlib import Path

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def parse_arguments() -> Path:
    """Parse commandline arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, help="The path to the input file.")
    args = parser.parse_args()
    return args.path


class Card:
    def __init__(self, *, value: int) -> None:
        self.value = value
        """The card value, as an integer."""

    def __str__(self) -> str:
        return f"{self.value}"

    @staticmethod
    def parse(string: str) -> Card:
        """Parse a card from a string."""
        match string:
            case "A":
                return Card(value=14)
            case "K":
                return Card(value=13)
            case "Q":
                return Card(value=12)
            case "J":
                return Card(value=11)
            case "T":
                return Card(value=10)
            case _:
                return Card(value=int(string))


class Hand:
    """A hand of camel cards."""

    def __init__(self, *, cards: list[Card], bid: int) -> None:
        self.cards = cards
        """The cards in the hand."""

        self.bid = bid
        """The hand bid."""

    @staticmethod
    def parse(string: str) -> Hand:
        """Parse a hand from a string."""
        cards, bid = string.split()
        return Hand(cards=[Card.parse(c) for c in cards], bid=int(bid))

    def strength(self) -> tuple[int, int]:
        """Compute the strength of the hand."""
        return self.type(), sum(
            c.value * 15**i for i, c in enumerate(self.cards[::-1])
        )

    def type(self) -> int:
        """Get the hand type identifier."""
        cards = defaultdict(int)
        for card in self.cards:
            cards[card.value] += 1

        n_combos = len(cards)
        max_cardinality = max(cards.values())

        # Five-of-a-kind
        if max_cardinality == 5:
            return 7
        # Four-of-a-kind
        if max_cardinality == 4:
            return 6
        # Full house
        if max_cardinality == 3 and n_combos == 2:
            return 5
        # Three-of-a-kind
        if max_cardinality == 3:
            return 4
        # Two pair
        if max_cardinality == 2 and n_combos == 3:
            return 3
        # One pair
        if max_cardinality == 2 and n_combos == 4:
            return 2

        # High card
        return 1

    def __str__(self) -> str:
        cards = "".join(f"[{c}]" for c in self.cards)
        return f"Hand(cards={cards}, bid={self.bid})"


def read_hands(path: Path) -> list[Hand]:
    """Read hands from a file."""
    return [Hand.parse(line) for line in path.open("r")]


def solve(path: Path) -> None:
    """Solve the puzzle."""
    hands = read_hands(path)
    hands = sorted(hands, key=Hand.strength)

    winnings = sum(hand.bid * (i + 1) for i, hand in enumerate(hands))
    print(winnings)


def main() -> int:
    path = parse_arguments()
    solve(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
