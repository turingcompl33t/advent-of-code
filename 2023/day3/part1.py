"""
part1.py

Advent of Code 2023 Day 3, Part 1.
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


class Symbol:
    """A symbol with its position."""

    def __init__(self, *, symbol: str, index: int) -> None:
        self.symbol = symbol
        """The symbol."""

        self.index = index
        """The index of the symbol."""

    def __str__(self) -> str:
        return f"Symbol(self.symbol={self.symbol}, index={self.index})"


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


def identify_symbols(line: str) -> list[Symbol]:
    """Identity the symbols in a line."""
    return [
        Symbol(symbol=c, index=i)
        for i, c in enumerate(line)
        if c != "." and not is_digit(c)
    ]


def is_adjacent_prev(candidate: Number, symbol: Symbol) -> bool:
    """Determine adjacency in a previous line."""
    return symbol.index in range(candidate.begin - 1, candidate.end + 2)


def is_adjacent_line(candidate: Number, symbol: Symbol) -> bool:
    """Determine adjacency in the current line."""
    return symbol.index + 1 == candidate.begin or symbol.index - 1 == candidate.end


def is_adjacent_next(candidate: Number, symbol: Symbol) -> bool:
    """Determine adjacency in the next line."""
    return symbol.index in range(candidate.begin - 1, candidate.end + 2)


def is_part_number(
    candidate: Number,
    symbols_prev: list[Symbol],
    symbols_line: list[Symbol],
    symbols_next: list[Symbol],
) -> list[Number]:
    """Determine if a number is a part number."""
    for symbol in symbols_prev:
        if is_adjacent_prev(candidate, symbol):
            return True
    for symbol in symbols_line:
        if is_adjacent_line(candidate, symbol):
            return True
    for symbol in symbols_next:
        if is_adjacent_next(candidate, symbol):
            return True

    return False


def extract_part_numbers(line: str, prev: Optional[str], next: Optional[str]) -> list[int]:
    """Extract part numbers from a triple of lines."""
    symbols_line = identify_symbols(line)
    symbols_prev = identify_symbols(prev) if prev is not None else []
    symbols_next = identify_symbols(next) if next is not None else []

    candidates = identify_numbers(line)
    return [
        num.value
        for num in candidates
        if is_part_number(num, symbols_prev, symbols_line, symbols_next)
    ]


def solve(path: Path) -> None:
    with path.open("r") as f:
        lines = f.readlines()
    lines = [line.strip("\n") for line in lines]

    count = 0
    for i in range(len(lines)):
        prev = lines[i - 1] if i > 0 else None
        next = lines[i + 1] if i < (len(lines) - 1) else None
        line = lines[i]
        count += sum(
            part_number for part_number in extract_part_numbers(line, prev, next)
        )

    print(count)


def main() -> int:
    path = parse_arguments()
    solve(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
