"""
part1.py

Advent of Code 2023, Day 18, Part 1.
"""

from __future__ import annotations

import sys
import argparse
from enum import Enum
from tqdm import tqdm
from pathlib import Path
from collections import namedtuple

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

INF = sys.maxsize


def parse_arguments() -> Path:
    """Parse commandline arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, help="The path to the input file.")
    args = parser.parse_args()
    return args.path


class Direction(Enum):
    R = "R"
    L = "L"
    U = "U"
    D = "D"

    @staticmethod
    def parse(string: str) -> Direction:
        """Parse a direction from a string."""
        match string:
            case "R":
                return Direction.R
            case "L":
                return Direction.L
            case "U":
                return Direction.U
            case "D":
                return Direction.D

    def __str__(self) -> str:
        return self.value


class Instruction:
    def __init__(self, *, direction: Direction, distance: int, color: str) -> None:
        self.direction = direction
        """The direction of the instruction"""

        self.distance = distance
        """The distance of the instruction"""

        self.color = color
        """The color code"""

    @staticmethod
    def parse(string: str) -> Instruction:
        """Parse an instruction from a string."""
        dir, dist, color = string.split()
        return Instruction(
            direction=Direction.parse(dir),
            distance=int(dist),
            color=color.removeprefix("(").removesuffix(")"),
        )

    def __str__(self) -> str:
        return f"Instr(dir={self.direction}, dist={self.distance}, color={self.color})"


Vertex = namedtuple("Vertex", "i j")


def read_dig_plan(path: Path) -> None:
    """Read the dig plan from file."""
    return [Instruction.parse(line.strip()) for line in path.open("r")]


def read_vertices(dig_plan: list[Instruction]) -> set[Vertex]:
    """Read vertices from dig plan."""
    position = Vertex(0, 0)
    vertices = [position]
    for instruction in dig_plan:
        match instruction.direction:
            case Direction.U:
                vertices.extend(
                    [
                        Vertex(position.i - d, position.j)
                        for d in range(instruction.distance + 1)
                    ]
                )
            case Direction.D:
                vertices.extend(
                    [
                        Vertex(position.i + d, position.j)
                        for d in range(instruction.distance + 1)
                    ]
                )
            case Direction.L:
                vertices.extend(
                    [
                        Vertex(position.i, position.j - d)
                        for d in range(instruction.distance + 1)
                    ]
                )
            case Direction.R:
                vertices.extend(
                    [
                        Vertex(position.i, position.j + d)
                        for d in range(instruction.distance + 1)
                    ]
                )
        position = vertices[-1]
    return set(vertices)


def limits(vertices: set[Vertex]) -> tuple[int, int, int, int]:
    """Compute limits of vertices."""
    mini = min(v.i for v in vertices)
    maxi = max(v.i for v in vertices)
    minj = min(v.j for v in vertices)
    maxj = max(v.j for v in vertices)
    return mini, maxi, minj, maxj


def inside(
    v: Vertex, vertices: list[Vertex], limits: tuple[int, int, int, int]
) -> bool:
    """Determine if an area of ground is inside the limits of the dig."""
    if v in vertices:
        return True

    enclosed_up = False
    for i in range(v.i, limits[0] - 1, -1):
        if Vertex(i, v.j) in vertices:
            enclosed_up = True

    enclosed_down = False
    for i in range(v.i, limits[1] + 1):
        if Vertex(i, v.j) in vertices:
            enclosed_down = True

    enclosed_left = False
    for j in range(v.j, limits[2] - 1, -1):
        if Vertex(v.i, j) in vertices:
            enclosed_left = True

    enclosed_right = False
    for j in range(v.j, limits[3] + 1):
        if Vertex(v.i, j) in vertices:
            enclosed_right = True

    return enclosed_up and enclosed_down and enclosed_left and enclosed_right


def solve(path: Path) -> None:
    """Solve the puzzle."""
    dig_plan = read_dig_plan(path)
    vertices = read_vertices(dig_plan)

    mini, maxi, minj, maxj = limits(vertices)

    count = 0
    for i in range(mini, maxi + 1):
        for j in range(minj, maxj + 1):
            if inside(Vertex(i, j), vertices, (mini, maxi, minj, maxj)):
                count += 1

    print(count)


def main() -> int:
    path = parse_arguments()
    solve(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
