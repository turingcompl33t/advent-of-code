"""
part1.py

Advent of Code 2023, Day 11, Part 1.
"""

from __future__ import annotations

import sys
import argparse
from enum import Enum
import itertools
from pathlib import Path

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# A sentinel value for floyd-warshall implementation
INF = sys.maxsize


def parse_arguments() -> Path:
    """Parse commandline arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, help="The path to the input file.")
    args = parser.parse_args()
    return args.path


class Symbol(Enum):
    """Symbol types."""

    GALAXY = "#"
    SPACE = "."

    @staticmethod
    def parse(string: str) -> Symbol:
        """Parse a symbol from a string."""
        match string:
            case "#":
                return Symbol.GALAXY
            case ".":
                return Symbol.SPACE
            case _:
                raise RuntimeError(f"unknown symbol '{string}'")

    def __str__(self) -> str:
        return self.value


def parse_need_expansion(map: list[list[Symbol]]) -> tuple[list[int, int]]:
    """Determine row and column indices that need expansion."""
    # Identity rows that need expansion
    rows = []
    for i, row in enumerate(map):
        if all(sym == Symbol.SPACE for sym in row):
            rows.append(i)

    # Identity columns that need expansion
    cols = []
    for col in range(len(map[0])):
        if all(map[row][col] == Symbol.SPACE for row in range(len(map))):
            cols.append(col)

    return rows, cols


def parse_galaxies(map: list[list[Symbol]]) -> list[tuple[int, int]]:
    """Get the positions of each galaxy."""
    positions = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == Symbol.GALAXY:
                positions.append((i, j))
    return positions


def expand_universe(
    galaxies: list[tuple[int, int]], rows: list[int], cols: list[int]
) -> list[tuple[int, int]]:
    """Expand the uninverse."""
    g = []
    for galaxy in galaxies:
        nrow = sum(1 for row in rows if row < galaxy[0])
        ncol = sum(1 for col in cols if col < galaxy[1])
        g.append((galaxy[0] + nrow, galaxy[1] + ncol))
    return g


def distance(g0: tuple[int, int], g1: tuple[int, int]) -> int:
    """Compute the distance between two galaxies."""
    return abs(g0[0] - g1[0]) + abs(g0[1] - g1[1])


def solve(path: Path) -> None:
    """Solve the puzzle."""
    map = [[Symbol.parse(c) for c in line.strip()] for line in path.open("r")]
    rows, cols = parse_need_expansion(map)

    galaxies = expand_universe(parse_galaxies(map), rows, cols)

    answer = sum(distance(*pair) for pair in itertools.combinations(galaxies, 2))
    print(answer)


def main() -> int:
    path = parse_arguments()
    solve(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
