"""
part1.py

Advent of Code 2023, Day 4, Part 1.
"""

from __future__ import annotations

import sys
import argparse
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

    @staticmethod
    def parse(string: str) -> Card:
        """Parse a card from a string."""
        id, numbers = string.split(":")

        winners, have = numbers.strip().split("|")
        return Card(
            id=int(id[-1]),
            winners=[int(n) for n in winners.strip().split()],
            have=[int(n) for n in have.strip().split()],
        )


def solve(path: Path) -> None:
    """Solve the puzzle."""
    count = sum(Card.parse(line.strip()).value() for line in path.open("r"))
    print(count)


def main() -> int:
    path = parse_arguments()
    solve(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
