"""
part2.py

Advent of Code 2023, Day 10, Part 2.
"""

from __future__ import annotations

import sys
import argparse
from typing import Optional
from enum import Enum
from pathlib import Path

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# A sentinel value for floyd-warshall implementation
INF = sys.maxsize


def parse_arguments() -> Path:
    """Parse commandline arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, help="The path to the input file.")
    args = parser.parse_args()
    return args.path


class Tile(Enum):
    """A tile."""

    VERTICAL_PIPE = "|"
    HORIZONTAL_PIPE = "-"
    BEND_NE = "L"
    BEND_NW = "J"
    BEND_SW = "7"
    BEND_SE = "F"
    GROUND = "."
    START = "S"

    @staticmethod
    def parse(string: str) -> Tile:
        """Parse a tile from a string."""
        match string:
            case "|":
                return Tile.VERTICAL_PIPE
            case "-":
                return Tile.HORIZONTAL_PIPE
            case "L":
                return Tile.BEND_NE
            case "J":
                return Tile.BEND_NW
            case "7":
                return Tile.BEND_SW
            case "F":
                return Tile.BEND_SE
            case ".":
                return Tile.GROUND
            case "S":
                return Tile.START
            case _:
                raise RuntimeError(f"unknown tile '{string}'")

    def __str__(self) -> str:
        return self.value


class Maze:
    """A parsed maze."""

    def __init__(self, *, tiles: list[list[Tile]]) -> None:
        self.tiles = tiles
        """The tiles in the maze."""

    @staticmethod
    def parse(lines: list[str]) -> Maze:
        """Parse a maze from a collection of lines."""
        return Maze(tiles=[[Tile.parse(c) for c in line] for line in lines])

    def tile(self, pos: tuple[int, int]) -> Tile:
        """Get the tile at the specified index."""
        return self.tiles[pos[0]][pos[1]]

    def interpolate_tile(self, pos: tuple[int, int]) -> Tile:
        """Interpolate the tile based on adjacent."""
        row = pos[0]
        col = pos[1]

        adjacent = self.adjacent(row, col)
        assert len(adjacent) == 2, "Broken invariant."

        above = (row - 1, col)
        below = (row + 1, col)
        left = (row, col - 1)
        right = (row, col + 1)

        if above in adjacent and below in adjacent:
            return Tile.VERTICAL_PIPE
        if left in adjacent and right in adjacent:
            return Tile.HORIZONTAL_PIPE
        if above in adjacent and right in adjacent:
            return Tile.BEND_NE
        if above in adjacent and left in adjacent:
            return Tile.BEND_NW
        if below in adjacent and left in adjacent:
            return Tile.BEND_SW
        if below in adjacent and right in adjacent:
            return Tile.BEND_SE

        raise RuntimeError("failed to interpolate tile")

    def loop(self) -> set[tuple[int, int]]:
        """Return a list of indices of tiles on the main loop."""
        start_position = self.start_index()
        adjacent = self.adjacent(*start_position)
        assert len(adjacent) == 2, "Broken invariant."

        # The tiles on the loop
        tiles: set[tuple[int, int]] = set()
        tiles.add(start_position)

        pos = adjacent[0]
        end = adjacent[1]

        tiles.add(pos)
        while pos != end:
            adjacent = self.adjacent(*pos)
            assert len(adjacent) == 2, "Broken invariant."

            a = adjacent[0]
            b = adjacent[1]

            if a in tiles:
                tiles.add(b)
                pos = b
            else:
                tiles.add(a)
                pos = a

        return tiles

    def adjacent(self, i: int, j: int) -> list[tuple[int, int]]:
        """Return the adjacent tiles based on input tile."""

        match self.tiles[i][j]:
            case Tile.VERTICAL_PIPE:
                adjacent = [adjacent_above(self, i, j), adjacent_below(self, i, j)]
            case Tile.HORIZONTAL_PIPE:
                adjacent = [adjacent_left(self, i, j), adjacent_right(self, i, j)]
            case Tile.BEND_NE:
                adjacent = [adjacent_above(self, i, j), adjacent_right(self, i, j)]
            case Tile.BEND_NW:
                adjacent = [adjacent_above(self, i, j), adjacent_left(self, i, j)]
            case Tile.BEND_SW:
                adjacent = [adjacent_below(self, i, j), adjacent_left(self, i, j)]
            case Tile.BEND_SE:
                adjacent = [adjacent_below(self, i, j), adjacent_right(self, i, j)]
            case Tile.GROUND:
                adjacent = []
            case Tile.START:
                adjacent = [
                    adjacent_above(self, i, j),
                    adjacent_below(self, i, j),
                    adjacent_left(self, i, j),
                    adjacent_right(self, i, j),
                ]

        adjacent = [a for a in adjacent if a is not None]
        assert len(adjacent) <= 2, "Broken postcondition."
        return adjacent

    def indices_of(self, tile: Tile) -> tuple[int, int]:
        """Get indices for specified tile type."""
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[i])):
                if self.tiles[i][j] == tile:
                    yield (i, j)

    def start_index(self) -> tuple[int, int]:
        """Get the index of the start tile."""
        for pos in self.indices_of(Tile.START):
            return pos


def adjacent_above(maze: Maze, i: int, j: int) -> Optional[tuple[int, int]]:
    """Determine the adjacent above."""
    if i == 0:
        return None

    above = maze.tiles[i - 1][j]
    if (
        above == Tile.VERTICAL_PIPE
        or above == Tile.BEND_SE
        or above == Tile.BEND_SW
        or above == Tile.START
    ):
        return (i - 1, j)

    return None


def adjacent_below(maze: Maze, i: int, j: int) -> Optional[tuple[int, int]]:
    """Determine adjacent below."""
    if i >= (len(maze.tiles) - 1):
        return None

    below = maze.tiles[i + 1][j]
    if (
        below == Tile.VERTICAL_PIPE
        or below == Tile.BEND_NE
        or below == Tile.BEND_NW
        or below == Tile.START
    ):
        return (i + 1, j)

    return None


def adjacent_left(maze: Maze, i: int, j: int) -> Optional[tuple[int, int]]:
    """Determine adjacent left."""
    if j == 0:
        return None

    left = maze.tiles[i][j - 1]
    if (
        left == Tile.HORIZONTAL_PIPE
        or left == Tile.BEND_NE
        or left == Tile.BEND_SE
        or left == Tile.START
    ):
        return (i, j - 1)

    return None


def adjacent_right(maze: Maze, i: int, j: int) -> Optional[tuple[int, int]]:
    """Determine adjacent right."""
    if j >= (len(maze.tiles[i]) - 1):
        return None

    right = maze.tiles[i][j + 1]
    if (
        right == Tile.HORIZONTAL_PIPE
        or right == Tile.BEND_NW
        or right == Tile.BEND_SW
        or right == Tile.START
    ):
        return (i, j + 1)

    return None


class State(Enum):
    """State for FSM."""

    OUT = "out"
    """Out of the loop."""

    IN_OPEN_EITHER = "open_either"
    """Open in either direction."""

    IN_OPEN_UP = "open_up"
    """Open in upward direction."""

    IN_OPEN_DOWN = "open_down"
    """Open in downward direction."""


#  case "|":
#     return Tile.VERTICAL_PIPE
# case "-":
#     return Tile.HORIZONTAL_PIPE
# case "L":
#     return Tile.BEND_NE
# case "J":
#     return Tile.BEND_NW
# case "7":
#     return Tile.BEND_SW
# case "F":
#     return Tile.BEND_SE
# case ".":
#     return Tile.GROUND


def process_tile(
    maze: Maze,
    pos: tuple[int, int],
    state: State,
    loop: set[tuple[int, int]],
    count: int,
) -> tuple[State, int]:
    """Process an individual tile."""
    on_loop = pos in loop
    inc_state = state in [State.IN_OPEN_UP, State.IN_OPEN_DOWN, State.IN_OPEN_EITHER]

    new_state = state

    tile = maze.tile(pos)

    match tile:
        case Tile.VERTICAL_PIPE:
            if on_loop:
                new_state = State.IN_OPEN_EITHER if not inc_state else state.OUT
            else:
                count = count + 1 if inc_state else count
        case Tile.HORIZONTAL_PIPE:
            if on_loop:
                pass
            else:
                count = count + 1 if inc_state else count
        case Tile.BEND_NE:
            if on_loop:
                new_state = State.OUT if inc_state else State.IN_OPEN_UP
            else:
                count = count + 1 if inc_state else count
        case Tile.BEND_NW:
            if on_loop:
                new_state = State.OUT
            else:
                count = count + 1 if inc_state else count
        case Tile.BEND_SW:
            if on_loop:
                new_state = State.OUT
            else:
                count = count + 1 if inc_state else count
        case Tile.BEND_SE:
            if on_loop:
                new_state = State.OUT if inc_state else State.IN_OPEN_DOWN
            else:
                count = count + 1 if inc_state else count
        case Tile.GROUND:
            return state, count + 1 if inc_state else count

    return new_state, count


def compute_loop_area(maze: Maze, loop: set[tuple[int, int]]) -> int:
    """Compute loop area."""
    n_row = len(maze.tiles)
    n_col = len(maze.tiles[0])

    count = 0
    state = State.OUT
    for row in range(n_row):
        for col in range(n_col):
            state, count = process_tile(maze, (row, col), state, loop, count)

    return count


def solve(_path: Path) -> None:
    """Solve the puzzle."""
    with _path.open("r") as f:
        lines = f.readlines()

    # Parse the maze
    maze = Maze.parse([line.strip() for line in lines])

    # Compute the maze primary loop
    loop = maze.loop()

    # Interpolate the maze start position
    start_row, start_col = maze.start_index()
    maze.tiles[start_row][start_col] = maze.interpolate_tile((start_row, start_col))

    area = compute_loop_area(maze, loop)
    print(area)


def main() -> int:
    path = parse_arguments()
    solve(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
