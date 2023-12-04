"""
part2.py

Advent of Code 2023, Day 4, Part 2.
"""

from __future__ import annotations

import re
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
    """A parsed card."""

    def __init__(self, *, id: int, winners: list[int], have: list[int]) -> None:
        self.id = id
        """The card ID."""

        self.winners = winners
        """The card winners."""

        self.have = have
        """The card have."""

    def value(self) -> int:
        """Determine the value of the card."""
        return int(2 ** (len(set(self.winners).intersection(set(self.have))) - 1))

    def matches(self) -> int:
        """Determine the cards matches."""
        return len(set(self.winners).intersection(self.have))

    @staticmethod
    def parse(string: str) -> Card:
        """Parse a card from a string."""
        id_string, numbers = string.split(":")

        matches = re.findall("[0-9]+", id_string)
        if len(matches) != 1:
            raise RuntimeError(f"failed to parse")

        winners, have = numbers.strip().split("|")
        return Card(
            id=int(matches[0]),
            winners=[int(n) for n in winners.strip().split()],
            have=[int(n) for n in have.strip().split()],
        )


def process_line(line: str, cards: defaultdict[int]) -> None:
    """Process a line."""
    card = Card.parse(line)

    cards[card.id] += 1
    for i in range(1, card.matches() + 1):
        cards[card.id + i] += cards[card.id]


def solve(path: Path) -> None:
    """Solve the puzzle."""
    # map Card ID -> instances
    cards = defaultdict(int)

    with path.open("r") as f:
        for line in f:
            line = line.strip()
            process_line(line, cards)

    print(sum(cards.values()))


def main() -> int:
    path = parse_arguments()
    solve(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
