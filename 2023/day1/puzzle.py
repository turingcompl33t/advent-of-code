"""
puzzle.py

Advent of Code 2023 Day 1.
"""

import typing
import sys
import regex as re
from enum import Enum, auto
import argparse
from pathlib import Path

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


class Part(Enum):
    ONE = auto()
    TWO = auto()


def parse_arguments() -> Path:
    """Parse commandline arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, help="The path to the input file.")
    args = parser.parse_args()
    return args.path


def parse_match(string: str) -> int:
    """
    Parse a match from a string.
    :param string: The input string:
    :return: The parsed digit
    """
    match string:
        case "one":
            return 1
        case "two":
            return 2
        case "three":
            return 3
        case "four":
            return 4
        case "five":
            return 5
        case "six":
            return 6
        case "seven":
            return 7
        case "eight":
            return 8
        case "nine":
            return 9
        case _:
            return int(string)


def parse_first_and_last_digit_part1(string: str) -> tuple[int, int]:
    """
    Parse the first and last digit from a string.
    :param string: The input string:
    :return: The parsed digit
    """
    matches = typing.cast(
        list[str],
        re.findall("[0-9]", string),
    )
    if len(matches) < 1:
        raise RuntimeError(f"insufficient matches in string {string}")
    return parse_match(matches[0]), parse_match(matches[-1])


def parse_first_and_last_digit_part2(string: str) -> tuple[int, int]:
    """
    Parse the first and last digit from a string.
    :param string: The input string:
    :return: The parsed digit
    """
    matches = typing.cast(
        list[str],
        re.findall(
            "([0-9]|one|two|three|four|five|six|seven|eight|nine)",
            string,
            overlapped=True,
        ),
    )
    if len(matches) < 1:
        raise RuntimeError(f"insufficient matches in string {string}")
    return parse_match(matches[0]), parse_match(matches[-1])


def parse_combined_digit(string: str, part: Part) -> int:
    """
    Parse the digit from a line.
    :param string: The input string:
    :return: The combined digit
    """
    if part == Part.ONE:
        f, l = parse_first_and_last_digit_part1(string)
    else:
        f, l = parse_first_and_last_digit_part2(string)
    return int(f"{f}{l}")


def solve_part1(path: Path) -> None:
    """Solve the puzzle."""
    with path.open("r") as f:
        s = sum(parse_combined_digit(line, Part.ONE) for line in f)
    print(s)


def solve_part2(path: Path) -> None:
    """Solve the puzzle."""
    with path.open("r") as f:
        s = sum(parse_combined_digit(line, Part.TWO) for line in f)
    print(s)


def main() -> int:
    path = parse_arguments()
    solve_part1(path)
    solve_part2(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
