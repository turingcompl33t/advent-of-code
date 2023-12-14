"""
part1.py

Advent of Code 2023, Day 14, Part 1.
"""

from __future__ import annotations

import sys
import argparse
from enum import Enum, auto
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


def read_rocks(path: Path) -> list[str]:
    """Read rocks from a file."""
    with path.open("r") as f:
        return [line.strip() for line in f]


def getrow(rocks: list[str], i: int) -> str:
    """Get a row from rocks."""
    return rocks[i]


def getcol(rocks: list[str], j: int) -> str:
    """Get a column from rocks."""
    return "".join(rocks[i][j] for i in range(len(rocks)))


def slide_one(string: str, index: int) -> str:
    """Slide a single rock in a string."""
    assert string[index] == "O", "Broken precondition."

    current = string
    for i in range(index - 1, -1, -1):
        if string[i] == ".":
            current = current[:i] + "O" + "." + current[i + 2 :]
        else:
            break

    return current


def slide_all(string: str) -> str:
    """Slide rocks in a string."""
    current = string
    for i in range(len(string)):
        if string[i] == "O":
            current = slide_one(current, i)
    return current


def tilt_north(rocks: list[str]) -> list[str]:
    """Move rocks by tilting the platform north."""
    cols = [slide_all(getcol(rocks, j)) for j in range(len(rocks[0]))]
    rows = [[col[i] for col in cols] for i in range(len(rocks))]
    return ["".join(row) for row in rows]


def weight(rocks: list[str]) -> int:
    """Compute the weight of the rocks."""
    return sum(
        sum(1 for rock in rocks[i] if rock == "O") * (len(rocks) - i)
        for i in range(len(rocks))
    )


def solve(path: Path) -> None:
    """Solve the puzzle."""
    rocks = read_rocks(path)

    w = weight(tilt_north(rocks))
    print(w)


def main() -> int:
    path = parse_arguments()
    solve(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
