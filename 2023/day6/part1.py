"""
part1.py

Advent of Code 2023, Day 6, Part 1.
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


def read_races(path: Path) -> list[Race]:
    """Read races from a file."""
    with path.open("r") as f:
        lines = f.readlines()

    assert len(lines) == 2, "Broken invariant"
    times, distances = lines

    times = times.split(":")[1].split()
    distances = distances.split(":")[1].split()

    return [
        Race(duration=int(times[i]), distance=int(distances[i]))
        for i in range(len(times))
    ]


def solve(path: Path) -> None:
    """Solve the puzzle."""
    races = read_races(path)

    answer = reduce(mul, [race.ways_to_win() for race in races], 1)
    print(answer)


def main() -> int:
    path = parse_arguments()
    solve(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
