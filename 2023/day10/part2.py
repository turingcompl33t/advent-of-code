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
import matplotlib.path as path

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

    def loop(self) -> list[tuple[int, int]]:
        """Return a list of indices of tiles on the main loop."""
        start_position = self.start_index()
        adjacent = self.adjacent(*start_position)
        assert len(adjacent) == 2, "Broken invariant."

        # The tiles on the loop
        tiles: list[tuple[int, int]] = []
        tiles.append(start_position)

        pos = adjacent[0]
        end = adjacent[1]

        tiles.append(pos)
        while pos != end:
            adjacent = self.adjacent(*pos)
            assert len(adjacent) == 2, "Broken invariant."

            a = adjacent[0]
            b = adjacent[1]

            if a in tiles:
                tiles.append(b)
                pos = b
            else:
                tiles.append(a)
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


def solve(_path: Path) -> None:
    """Solve the puzzle."""
    with _path.open("r") as f:
        lines = f.readlines()

    # Parse the maze
    maze = Maze.parse([line.strip() for line in lines])

    # Compute the maze primary loop
    loop = maze.loop()

    # Create polygon to test loop membership
    polygon = path.Path(loop)
    # Convert to set for fast lookup
    loop = set(loop)

    count = 0
    for i in range(len(maze.tiles)):
        for j in range(len(maze.tiles[0])):
            if (i, j) in loop:
                continue
            if polygon.contains_point((i, j)):
                count += 1

    print(count)


def main() -> int:
    path = parse_arguments()
    solve(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
