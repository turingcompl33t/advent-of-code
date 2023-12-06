"""
part2.py

Advent of Code 2023, Day 6, Part 2.
"""

import sys
import argparse
from functools import reduce
from operator import mul
from pathlib import Path

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def parse_arguments() -> Path:
    """Parse commandline arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, help="The path to the input file.")
    args = parser.parse_args()
    return args.path


def distance_covered(hold_duration: int, race_duration: int) -> int:
    """Calculate the distance covered in a race for a given hold duration."""
    return (race_duration - hold_duration) * hold_duration


class Race:
    """A description of a race."""

    def __init__(self, *, duration: int, distance: int) -> None:
        self.duration = duration
        """The duration of this race."""

        self.distance = distance
        """The record distance in this race."""

    def ways_to_win(self) -> int:
        """Return the number of ways the race can be won."""
        return sum(
            1
            for hold_time in range(self.duration)
            if distance_covered(hold_time, self.duration) > self.distance
        )

    def __str__(self) -> str:
        return f"Race(duration={self.duration}, distance={self.distance})"


def read_race(path: Path) -> Race:
    """Read race from a file."""
    with path.open("r") as f:
        lines = f.readlines()

    assert len(lines) == 2, "Broken invariant"
    times, distances = lines

    time = "".join(times.split(":")[1].split())
    distance = "".join(distances.split(":")[1].split())

    return Race(duration=int(time), distance=int(distance))


def solve(path: Path) -> None:
    """Solve the puzzle."""
    race = read_race(path)
    print(race.ways_to_win())


def main() -> int:
    path = parse_arguments()
    solve(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
