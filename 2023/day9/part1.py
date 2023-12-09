"""
part1.py

Advent of Code 2023, Day 9, Part 1.
"""

from __future__ import annotations

import sys
import argparse
import numpy as np
from pathlib import Path

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def parse_arguments() -> Path:
    """Parse commandline arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, help="The path to the input file.")
    args = parser.parse_args()
    return args.path


def parse_sequences(path: Path) -> list[np.ndarray]:
    """Parse sequences from a file."""
    return [np.array([int(v) for v in line.strip().split()]) for line in path.open("r")]


def diff(seq: np.ndarray) -> np.ndarray:
    """Compute the difference for a sequence."""
    if len(seq) < 2:
        raise RuntimeError("sequence too short")
    return np.diff(seq)


def compute_next_value(seq: np.ndarray) -> int:
    """Compute the next value for a sequence."""
    _diff = diff(seq)
    if np.all(seq == 0):
        return 0

    return seq[-1] + compute_next_value(_diff)


def solve(path: Path) -> None:
    """Solve the puzzle."""
    seqs = parse_sequences(path)

    solution = sum(compute_next_value(seq) for seq in seqs)
    print(solution)


def main() -> int:
    path = parse_arguments()
    solve(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
