"""
part1.py

Advent of Code 2023, Day 16, Part 1.
"""

from __future__ import annotations

import sys
from enum import Enum
import argparse
from pathlib import Path
from typing import Optional

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def parse_arguments() -> Path:
    """Parse commandline arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, help="The path to the input file.")
    args = parser.parse_args()
    return args.path


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def __str__(self) -> str:
        return str(self.name)


class Beam:
    """Represents a beam."""

    def __init__(self, *, pos: tuple[int, int], dir: Direction) -> None:
        self.pos = pos
        """The position of the beam."""

        self.dir = dir
        """The direction of the beam."""

    def __hash__(self) -> int:
        return hash((self.pos[0], self.pos[1], self.dir.value))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Beam):
            return False
        return self.pos == other.pos and self.dir == other.dir

    def __neq__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"Beam(pos={self.pos}, dir={self.dir})"


def read_grid(path: Path) -> list[str]:
    """Read the grid from file."""
    return [line.strip() for line in path.open("r")]


def up(grid: list[str], beam: Beam) -> Optional[Beam]:
    """Return a beam moved up one position."""
    row = beam.pos[0]
    col = beam.pos[1]
    return Beam(pos=(row - 1, col), dir=Direction.UP) if row - 1 >= 0 else None


def down(grid: list[str], beam: Beam) -> Optional[Beam]:
    """Return a beam moved down one position."""
    row = beam.pos[0]
    col = beam.pos[1]
    return Beam(pos=(row + 1, col), dir=Direction.DOWN) if row + 1 < len(grid) else None


def left(grid: list[str], beam: Beam) -> Optional[Beam]:
    """Return a beam moved left one position."""
    row = beam.pos[0]
    col = beam.pos[1]
    return Beam(pos=(row, col - 1), dir=Direction.LEFT) if col - 1 >= 0 else None


def right(grid: list[str], beam: Beam) -> Optional[Beam]:
    """Return a beam moved right one position."""
    row = beam.pos[0]
    col = beam.pos[1]
    return (
        Beam(pos=(row, col + 1), dir=Direction.RIGHT)
        if col + 1 < len(grid[0])
        else None
    )


def update_beam_up(grid: list[str], beam: Beam) -> list[Beam]:
    """Update a beam moving up."""
    assert beam.dir == Direction.UP, "Broken precondition."
    match grid[beam.pos[0]][beam.pos[1]]:
        case ".":
            return [up(grid, beam)]
        case "|":
            return [up(grid, beam)]
        case "-":
            return [left(grid, beam), right(grid, beam)]
        case "/":
            return [right(grid, beam)]
        case "\\":
            return [left(grid, beam)]


def update_beam_down(grid: list[str], beam: Beam) -> list[Beam]:
    """Update a beam moving down."""
    assert beam.dir == Direction.DOWN, "Broken precondition."
    match grid[beam.pos[0]][beam.pos[1]]:
        case ".":
            return [down(grid, beam)]
        case "|":
            return [down(grid, beam)]
        case "-":
            return [left(grid, beam), right(grid, beam)]
        case "/":
            return [left(grid, beam)]
        case "\\":
            return [right(grid, beam)]


def update_beam_left(grid: list[str], beam: Beam) -> list[Beam]:
    """Update a beam moving left."""
    assert beam.dir == Direction.LEFT, "Broken precondition."
    match grid[beam.pos[0]][beam.pos[1]]:
        case ".":
            return [left(grid, beam)]
        case "|":
            return [up(grid, beam), down(grid, beam)]
        case "-":
            return [left(grid, beam)]
        case "/":
            return [down(grid, beam)]
        case "\\":
            return [up(grid, beam)]


def update_beam_right(grid: list[str], beam: Beam) -> list[Beam]:
    """Update a beam moving right."""
    assert beam.dir == Direction.RIGHT, "Broken precondition."
    match grid[beam.pos[0]][beam.pos[1]]:
        case ".":
            return [right(grid, beam)]
        case "|":
            return [up(grid, beam), down(grid, beam)]
        case "-":
            return [right(grid, beam)]
        case "/":
            return [up(grid, beam)]
        case "\\":
            return [down(grid, beam)]


def update(grid: list[str], beam: Beam) -> list[Beam]:
    """Update a beam."""
    match beam.dir:
        case Direction.UP:
            return update_beam_up(grid, beam)
        case Direction.DOWN:
            return update_beam_down(grid, beam)
        case Direction.LEFT:
            return update_beam_left(grid, beam)
        case Direction.RIGHT:
            return update_beam_right(grid, beam)


def trace_beam(
    grid: list[str], beam: Beam, energized: set[tuple[int, int]]
) -> list[Beam]:
    """Trace a beam through the grid."""
    while True:
        energized.add(beam.pos)

        # Update the position of the beam
        updated = update(grid, beam)
        updated = [b for b in updated if b is not None]

        # Processing complete
        if len(updated) == 0:
            return []

        # Split beam
        if len(updated) == 2:
            return [updated[0], updated[1]]

        # Single beam continues
        assert len(updated) == 1, "Broken invariant."
        beam = updated[0]


def n_energized(grid: list[str]) -> int:
    """Compute energized cells."""
    energized: set[tuple[int, int]] = set()

    in_progress: list[Beam] = [Beam(pos=(0, 0), dir=Direction.RIGHT)]

    all_beams: set[Beam] = set(in_progress)
    while len(in_progress) > 0:
        new_beams = trace_beam(grid, in_progress.pop(0), energized)

        for new_beam in new_beams:
            if new_beam not in all_beams:
                all_beams.add(new_beam)
                in_progress.append(new_beam)

    return len(energized)


def solve(path: Path) -> None:
    """Solve the puzzle."""
    grid = read_grid(path)

    count = n_energized(grid)
    print(count)


def main() -> int:
    path = parse_arguments()
    solve(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
