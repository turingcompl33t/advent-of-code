"""
part2.py

Advent of Code 2023, Day 12, Part 2.
"""

from __future__ import annotations

import functools
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


def parse_row(string: str) -> tuple[str, list[int]]:
    """Parse a from string."""
    springs, numbers = string.split()
    springs = "?".join([springs] * 5)
    numbers = [int(n) for n in numbers.split(",")] * 5
    return springs, tuple(numbers)


def read_rows(path: Path) -> list[tuple[str, list[int]]]:
    """Read rows from file."""
    return [parse_row(line.strip()) for line in path.open("r")]


@functools.cache
def arrangements(springs: str, numbers: list[int], run_length: int) -> int:
    """Determine the possible arrangements for the given configuration."""
    # Base case: got all runs
    if len(numbers) == 0:
        return 0 if any(c == "#" for c in springs) else 1

    # Base case: end of input
    if len(springs) == 0:
        return 0

    in_run = run_length > 0
    match springs[0]:
        case ".":
            if in_run and run_length == numbers[0]:
                return arrangements(springs[1:], numbers[1:], 0)
            return 0 if in_run else arrangements(springs[1:], numbers, 0)
        case "#":
            return arrangements(springs[1:], numbers, run_length + 1)
        case "?":
            return arrangements("." + springs[1:], numbers, run_length) + arrangements(
                "#" + springs[1:], numbers, run_length
            )
        case _:
            raise RuntimeError("unreachable")


def solve(path: Path) -> None:
    """Solve the puzzle."""
    rows = read_rows(path)
    # Add a terminator for processing purposes
    rows = [(springs + ".", numbers) for springs, numbers in rows]

    count = sum(arrangements(springs, numbers, 0) for springs, numbers in rows)
    print(count)


def main() -> int:
    path = parse_arguments()
    solve(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
