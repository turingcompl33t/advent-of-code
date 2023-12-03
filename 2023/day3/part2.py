"""
part2.py

Advent of Code 2023 Day 3, Part 2.
"""

from __future__ import annotations

import re
import sys
import argparse
from typing import Optional
from pathlib import Path

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def parse_arguments() -> Path:
    """Parse commandline arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, help="The path to the input file.")
    args = parser.parse_args()
    return args.path


class Number:
    """A number with its position."""

    def __init__(self, *, value: int, begin: int, end: int) -> None:
        self.value = value
        """The numeric value."""

        self.begin = begin
        """The begin index."""

        self.end = end
        """The end index."""

    def __str__(self) -> str:
        return f"Number(self.value={self.value}, pos=({self.begin}, {self.end}))"


class Gear:
    """A gear symbol with its position."""

    def __init__(self, *, index: int) -> None:
        self.index = index
        """The index of the gear."""

    def __str__(self) -> str:
        return f"Gear(index={self.index})"


def is_digit(c: str) -> bool:
    """Determine if a character is a digit."""
    try:
        int(c)
        return True
    except ValueError:
        return False


def identify_numbers(line: str) -> list[Number]:
    """Identity the numbers in a line."""
    numbers = []
    for m in re.finditer("[0-9]+", line):
        begin, end = m.span()
        numbers.append(Number(value=int(m.group()), begin=begin, end=end - 1))
    return numbers


def identify_gears(line: str) -> list[Gear]:
    """Identity the symbols in a line."""
    return [Gear(index=i) for i, c in enumerate(line) if c == "*"]


def is_adjacent_prev(candidate: Gear, number: Number) -> bool:
    """Determine adjacency in a previous line."""
    return candidate.index in range(number.begin - 1, number.end + 2)


def is_adjacent_line(candidate: Gear, number: Number) -> bool:
    """Determine adjacency in the current line."""
    return candidate.index + 1 == number.begin or candidate.index - 1 == number.end


def is_adjacent_next(candidate: Gear, number: Number) -> bool:
    """Determine adjacency in the next line."""
    return candidate.index in range(number.begin - 1, number.end + 2)


def is_gear(
    candidate: Gear,
    numbers_prev: list[Number],
    numbers_line: list[Number],
    numbers_next: list[Number],
) -> tuple[bool, Optional[Number], Optional[Number]]:
    """Determine if a symbol is a true gear."""
    adjacent = []

    for number in numbers_prev:
        if is_adjacent_prev(candidate, number):
            adjacent.append(number)

    for number in numbers_line:
        if is_adjacent_line(candidate, number):
            adjacent.append(number)

    for number in numbers_next:
        if is_adjacent_next(candidate, number):
            adjacent.append(number)

    if len(adjacent) == 2:
        return True, adjacent[0], adjacent[1]

    return False, None, None


def extract_gear_ratios(line: str, prev: Optional[str], next: Optional[str]) -> int:
    """Extract gear ratios from a triple of lines."""
    numbers_line = identify_numbers(line)
    numbers_prev = identify_numbers(prev) if prev is not None else []
    numbers_next = identify_numbers(next) if next is not None else []

    gear_ratio_sum = 0
    for candidate in identify_gears(line):
        _is_gear, gear0, gear1 = is_gear(
            candidate, numbers_prev, numbers_line, numbers_next
        )
        if _is_gear:
            gear_ratio_sum += gear0.value * gear1.value

    return gear_ratio_sum


def solve(path: Path) -> None:
    with path.open("r") as f:
        lines = f.readlines()
    lines = [line.strip("\n") for line in lines]

    count = 0
    for i in range(len(lines)):
        prev = lines[i - 1] if i > 0 else None
        next = lines[i + 1] if i < (len(lines) - 1) else None
        line = lines[i]

        count += extract_gear_ratios(line, prev, next)

    print(count)


def main() -> int:
    path = parse_arguments()
    solve(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
