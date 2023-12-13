"""
part2.py

Advent of Code 2023, Day 13, Part 2.
"""

from __future__ import annotations

import sys
import argparse
from enum import Enum, auto
import itertools
from typing import Optional
from pathlib import Path

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


class Axis(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()


def parse_arguments() -> Path:
    """Parse commandline arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, help="The path to the input file.")
    args = parser.parse_args()
    return args.path


def read_patterns(path: Path) -> list[list[str]]:
    """Read patterns from a file."""
    with path.open("r") as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]
    lines = [list(g) for _, g in itertools.groupby(lines, key="".__ne__)]
    lines = [g for g in lines if len(g) > 1]
    return lines


def nrows(pattern: list[str]) -> int:
    """Get the number of rows in a pattern."""
    return len(pattern)


def ncols(pattern: list[str]) -> int:
    """Get the number of columns in a pattern."""
    return len(pattern[0])


def getrow(pattern: list[str], i: int) -> str:
    """Get a row from a pattern."""
    return pattern[i]


def getcol(pattern: list[str], j: int) -> str:
    """Get a column from a pattern."""
    return "".join(pattern[i][j] for i in range(len(pattern)))


def is_reflected_across_index(string: str, i: int) -> bool:
    """Determine if a string is reflected across an index."""
    a = string[: i + 1][::-1]
    b = string[i + 1 :]
    for i in range(min(len(a), len(b))):
        if a[i] != b[i]:
            return False
    return True


def is_reflected_across_row(pattern: list[str], row: int) -> bool:
    """Determine if the pattern is reflected across row."""
    return all(
        is_reflected_across_index(getcol(pattern, j), row)
        for j in range(ncols(pattern))
    )


def is_reflected_across_col(pattern: list[str], col: int) -> bool:
    """Determine if the pattern is reflected across col."""
    return all(
        is_reflected_across_index(getrow(pattern, i), col)
        for i in range(nrows(pattern))
    )


def axis_of_reflection(
    pattern: list[str], blacklist: Optional[tuple[Axis, int]] = None
) -> Optional[tuple[Axis, int]]:
    """Compute the axis of reflection for a pattern."""
    for i in range(nrows(pattern) - 1):
        if is_reflected_across_row(pattern, i):
            candidate = (Axis.HORIZONTAL, i)
            if blacklist is None or candidate != blacklist:
                return candidate

    for j in range(ncols(pattern) - 1):
        if is_reflected_across_col(pattern, j):
            candidate = (Axis.VERTICAL, j)
            if blacklist is None or candidate != blacklist:
                return candidate

    return None


def clean_smudge(pattern: list[str], loc: tuple[int, int]) -> list[str]:
    """Clean a smudge from a pattern."""
    sym = "." if pattern[loc[0]][loc[1]] == "#" else "#"
    return [
        row[: loc[1]] + sym + row[loc[1] + 1 :] if i == loc[0] else row
        for i, row in enumerate(pattern)
    ]


def axis_of_reflection_with_cleaning(pattern: list[str]) -> tuple[Axis, int]:
    """Compute the axis of reflection, with smudge fixing."""
    original = axis_of_reflection(pattern)
    for i in range(nrows(pattern)):
        for j in range(ncols(pattern)):
            p = clean_smudge(pattern, (i, j))

            a = axis_of_reflection(p, original)
            if a is not None and a != original:
                return a

    raise RuntimeError("no reflection found")


def summarize(reflection_data: tuple[Axis, int]) -> int:
    """Summarize reflection data."""
    return (
        reflection_data[1] + 1
        if reflection_data[0] == Axis.VERTICAL
        else (reflection_data[1] + 1) * 100
    )


def solve(path: Path) -> None:
    """Solve the puzzle."""
    patterns = read_patterns(path)

    summary = sum(summarize(axis_of_reflection_with_cleaning(p)) for p in patterns)
    print(summary)


def main() -> int:
    path = parse_arguments()
    solve(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
