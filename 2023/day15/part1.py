"""
part1.py

Advent of Code 2023, Day 15, Part 1.
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


def read_initialization_sequence(path: Path) -> list[str]:
    """Read the initialization sequence."""
    sequence: list[str] = []
    with path.open("r") as f:
        for line in f:
            sequence.extend(line.strip().split(","))
    return sequence


def hash(string: str) -> int:
    """Get the hash value for a string."""
    current = 0
    for c in string:
        current = ((current + ord(c))) * 17 % 256
    return current


def solve(path: Path) -> None:
    """Solve the puzzle."""
    sequence = read_initialization_sequence(path)
    result = sum(hash(step) for step in sequence)
    print(result)


def main() -> int:
    path = parse_arguments()
    solve(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
