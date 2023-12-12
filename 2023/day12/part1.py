"""
part1.py

Advent of Code 2023, Day 12, Part 1.
"""

from __future__ import annotations

import sys
import argparse
from enum import Enum
import itertools
from pathlib import Path

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def parse_arguments() -> Path:
    """Parse commandline arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, help="The path to the input file.")
    args = parser.parse_args()
    return args.path


class Symbol(Enum):
    """Parsed symbols."""

    OPERATIONAL = "."
    BROKEN = "#"
    UNKNOWN = "?"

    @staticmethod
    def parse(string: str) -> Symbol:
        match string:
            case ".":
                return Symbol.OPERATIONAL
            case "#":
                return Symbol.BROKEN
            case "?":
                return Symbol.UNKNOWN
            case _:
                raise RuntimeError(f"unknown symbol '{string}'")

    def __str__(self) -> str:
        return self.value


class SpringRow:
    """The information for a row of springs."""

    def __init__(self, *, symbols: list[Symbol], numbers: list[int]) -> None:
        self.symbols = symbols
        """The symbols for the row."""

        self.numbers = numbers
        """The numbers for the row."""

    @staticmethod
    def parse(string: str) -> str:
        """Parse from a string."""
        symbols, numbers = string.split()
        return SpringRow(
            symbols=[Symbol.parse(c) for c in symbols],
            numbers=[int(c) for c in numbers.split(",")],
        )


def read_rows(path: Path) -> list[SpringRow]:
    """Read rows from file."""
    with path.open("r") as f:
        return [SpringRow.parse(line.strip()) for line in f]


def candidates(row: SpringRow) -> list[Symbol]:
    """Compute candidate sequences."""

    positions = []
    for symbol in row.symbols:
        if symbol == Symbol.UNKNOWN:
            positions.append([Symbol.BROKEN, Symbol.OPERATIONAL])
        else:
            positions.append([symbol])

    for sequence in itertools.product(*positions):
        yield list(sequence)


def broken_positions(symbols: list[Symbol]) -> list[int]:
    """Compute a sequence of the broken runs in the list of symbols."""
    runs = []
    in_run = False
    run_length = 0
    for symbol in symbols:
        if symbol == Symbol.OPERATIONAL:
            if in_run:
                runs.append(run_length)
                run_length = 0
                in_run = False
        else:
            run_length += 1
            in_run = True

    if in_run:
        runs.append(run_length)

    return runs


def possible_arrangements(row: SpringRow) -> int:
    """Compute the possible arrangements for a row."""
    return sum(
        1 for candidate in candidates(row) if broken_positions(candidate) == row.numbers
    )


def solve(path: Path) -> None:
    """Solve the puzzle."""
    rows = read_rows(path)
    count = sum(possible_arrangements(row) for row in rows)
    print(count)

def main() -> int:
    path = parse_arguments()
    solve(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
