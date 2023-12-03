"""
puzzle.py

Advent of Code 2023 Day 2.
"""

from __future__ import annotations

import sys
import argparse
from operator import mul
from pathlib import Path
import functools
from enum import Enum, auto

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


class Color(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()

    @staticmethod
    def parse(string: str) -> Color:
        """ "Parse from a string."""
        match string:
            case "red":
                return Color.RED
            case "green":
                return Color.GREEN
            case "blue":
                return Color.BLUE
            case _:
                raise RuntimeError(f"invalid color '{string}'")


class Trial:
    """A parsed trial from a game."""

    def __init__(self, *, colors: dict[Color, int]) -> None:
        self.colors = colors

    @staticmethod
    def parse(string: str) -> Trial:
        """Parse a trial from a string."""
        mapped = {}
        for color in [c.strip(" ") for c in string.split(",")]:
            count, c = color.split(" ")
            mapped[Color.parse(c)] = int(count)
        return Trial(colors=mapped)


class Game:
    """A parsed game."""

    def __init__(self, *, id: int, trials: list[Trial]) -> None:
        self.id = id
        self.trials = trials

    @staticmethod
    def parse(string: str) -> Game:
        """Parse a game from a string."""
        id, trials = string.split(":")
        return Game(
            id=int(id.removeprefix("Game ")),
            trials=[Trial.parse(t) for t in trials.split(";")],
        )

    def is_possible(self, constraints: dict[Color, int]) -> bool:
        """Determine if this game is possible with a certain number of cubes."""
        for trial in self.trials:
            for color, count in constraints.items():
                if color not in trial.colors:
                    continue
                if trial.colors[color] > count:
                    return False

        return True
    
    def fewest_possible(self) -> dict[Color, int]:
        """Determine the fewest possible cubes with which the game could have been played."""
        fewest = {}
        for color in Color:
            m = max(trial.colors[color] if color in trial.colors else 0 for trial in self.trials)
            fewest[color] = m
        return fewest


def parse_arguments() -> Path:
    """Parse commandline arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, help="The path to the input file.")
    args = parser.parse_args()
    return args.path

def power(cubes: dict[Color, int]) -> int:
    """Compute the power of a set of cubes."""
    return functools.reduce(mul, cubes.values(), 1)

def solve_part1(path: Path):
    """Solve Part 1."""
    count = 0
    with path.open("r") as f:
        for line in f:
            g = Game.parse(line.strip("\n"))
            if g.is_possible({Color.RED: 12, Color.GREEN: 13, Color.BLUE: 14}):
                count += g.id
    print(count)

def solve_part2(path: Path) -> None:
    """Solve Part 2."""
    count = 0
    with path.open("r") as f:
        for line in f:
            g = Game.parse(line.strip("\n"))
            count += power(g.fewest_possible())
    print(count)

def main() -> int:
    path = parse_arguments()
    # solve_part1(path)
    solve_part2(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
