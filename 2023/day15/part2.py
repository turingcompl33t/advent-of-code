"""
part2.py

Advent of Code 2023, Day 15, Part 2.
"""

from __future__ import annotations

import sys
import argparse
from typing import Optional
from pathlib import Path
from collections import defaultdict

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def parse_arguments() -> Path:
    """Parse commandline arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, help="The path to the input file.")
    args = parser.parse_args()
    return args.path


class Step:
    """A parsed step."""

    def __init__(
        self, *, lens_label: str, operation: str, focal_length: Optional[int] = None
    ):
        assert (
            operation == "-"
            and focal_length is None
            or operation == "="
            and focal_length is not None
        ), "Broken precondition."

        self.lens_label = lens_label
        """The lens label."""

        self.operation = operation
        """The operation identifier."""

        self._focal_length = focal_length
        """The focal length."""

    @property
    def focal_length(self) -> int:
        if self._focal_length is None:
            raise RuntimeError("no focal length")
        return self._focal_length

    @staticmethod
    def parse(string: str) -> Step:
        """Parse a step from a string."""
        if string.find("-") != -1:
            lens_label, _ = string.split("-")
            return Step(lens_label=lens_label, operation="-")
        lens_label, focal_length = string.split("=")
        return Step(
            lens_label=lens_label, operation="=", focal_length=int(focal_length)
        )


def read_initialization_sequence(path: Path) -> list[Step]:
    """Read the initialization sequence."""
    sequence: list[str] = []
    with path.open("r") as f:
        for line in f:
            sequence.extend(line.strip().split(","))
    return [Step.parse(step) for step in sequence]


def hash(string: str) -> int:
    """Get the hash value for a string."""
    current = 0
    for c in string:
        current = ((current + ord(c))) * 17 % 256
    return current


def find_lens(label: str, box_contents: list[tuple[str, int]]) -> int:
    """Find a lens in a box."""
    for i, (lens_label, _) in enumerate(box_contents):
        if lens_label == label:
            return i
    # Not found
    return -1


def process_step(step: Step, state: dict[int, list[tuple[str, int]]]) -> None:
    """Process a step in the initialization sequence."""
    boxno = hash(step.lens_label)

    if step.operation == "-":
        index = find_lens(step.lens_label, state[boxno])
        if index == -1:
            return
        # Remove the lens from the box
        _ = state[boxno].pop(index)
    elif step.operation == "=":
        index = find_lens(step.lens_label, state[boxno])
        if index == -1:
            # Add the lens to the back of the box
            state[boxno].append((step.lens_label, step.focal_length))
        else:
            # Replace the lens
            state[boxno][index] = (step.lens_label, step.focal_length)


def focusing_power_box(boxno: int, contents: list[tuple[str, int]]) -> int:
    """Compute the focusing power for a box."""
    return sum((1 + boxno) * (i + 1) * contents[i][1] for i in range(len(contents)))


def focusing_power(state: dict[int, list[tuple[str, int]]]) -> int:
    """Compute the focusing power of all lenses."""
    return sum(focusing_power_box(boxno, contents) for boxno, contents in state.items())


def solve(path: Path) -> None:
    """Solve the puzzle."""
    steps = read_initialization_sequence(path)

    # A map {BOXNO -> {LENSLABEL -> FOCALLENGTH}}
    state: dict[int, list[tuple[str, int]]] = defaultdict(list)
    for step in steps:
        process_step(step, state)

    power = focusing_power(state)
    print(power)


def main() -> int:
    path = parse_arguments()
    solve(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
