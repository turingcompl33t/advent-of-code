"""
part2.py

Advent of Code 2023, Day 17, Part 2.
"""

from __future__ import annotations

import sys
import argparse
from tqdm import tqdm
import heapq
import itertools
from enum import Enum
from pathlib import Path
from typing import Optional
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


def read_map(path: Path) -> list[list[int]]:
    """Read the map from file."""
    with path.open("r") as f:
        return [[int(c) for c in line.strip()] for line in f]


class Direction(Enum):
    """An enumeration over directions."""

    U = "up"
    D = "down"
    L = "left"
    R = "right"

    @staticmethod
    def opposite(d: Direction) -> Direction:
        """Compute the opposite of a direction."""
        match d:
            case Direction.U:
                return Direction.D
            case Direction.D:
                return Direction.U
            case Direction.L:
                return Direction.R
            case Direction.R:
                return Direction.L

    @staticmethod
    def left(d: Direction) -> Direction:
        """Compute left of direction."""
        match d:
            case Direction.U:
                return Direction.L
            case Direction.D:
                return Direction.R
            case Direction.L:
                return Direction.D
            case Direction.R:
                return Direction.U

    @staticmethod
    def right(d: Direction) -> Direction:
        """Compute right of direction."""
        match d:
            case Direction.U:
                return Direction.R
            case Direction.D:
                return Direction.L
            case Direction.L:
                return Direction.U
            case Direction.R:
                return Direction.D


# (i, j, direction, streak)
Vertex = namedtuple("Vertex", "i j d s")


def up(map: list[list[int]], i: int, j: int) -> Optional[tuple[int, int]]:
    """Return the point in the Up direction."""
    return (i - 1, j) if i - 1 >= 0 else None


def down(map: list[list[str]], i: int, j: int) -> Optional[tuple[int, int]]:
    """Return the point in the Down direction."""
    return (i + 1, j) if i + 1 < len(map) else None


def left(map: list[list[str]], i: int, j: int) -> Optional[tuple[int, int]]:
    """Return the point in the Left direction."""
    return (i, j - 1) if j - 1 >= 0 else None


def right(map: list[list[int]], i: int, j: int) -> Optional[tuple[int, int]]:
    """Return the point in the Right direction."""
    return (i, j + 1) if j + 1 < len(map[0]) else None


def adjacent(map: list[list[int]], v: Vertex) -> tuple[list[int], list[Vertex]]:
    """Compute adjacent vertices to v."""
    adjacent: list[Vertex] = []

    u = up(map, v.i, v.j)
    if u is not None:
        adjacent.append(
            Vertex(u[0], u[1], Direction.U, v.s + 1 if v.d == Direction.U else 1)
        )

    d = down(map, v.i, v.j)
    if d is not None:
        adjacent.append(
            Vertex(d[0], d[1], Direction.D, v.s + 1 if v.d == Direction.D else 1)
        )

    l = left(map, v.i, v.j)
    if l is not None:
        adjacent.append(
            Vertex(l[0], l[1], Direction.L, v.s + 1 if v.d == Direction.L else 1)
        )

    r = right(map, v.i, v.j)
    if r is not None:
        adjacent.append(
            Vertex(r[0], r[1], Direction.R, v.s + 1 if v.d == Direction.R else 1)
        )

    adjacent = [
        a
        for a in adjacent
        if (a.d == v.d and a.s <= 10)
        or (a.d == Direction.right(v.d) and v.s >= 4)
        or (a.d == Direction.left(v.d) and v.s >= 4)
    ]

    return [map[a.i][a.j] for a in adjacent], adjacent


def distance(map: list[list[int]], src: Vertex, dst: Vertex) -> int:
    """Compute shortest distance from src to dst."""
    dist: dict[Vertex, int] = {}
    for i in range(len(map)):
        for j in range(len(map[0])):
            for d in [Direction.U, Direction.D, Direction.L, Direction.R]:
                for s in range(0, 11):
                    dist[Vertex(i, j, d, s)] = INF

    dist[src] = 0

    q = [(0, 0, src)]
    c = 1
    while len(q) > 0:
        weight, _, u = heapq.heappop(q)

        if u == dst:
            return weight

        ws, vs = adjacent(map, u)
        for w, v in zip(ws, vs):
            alt = weight + w
            if alt < dist[v]:
                heapq.heappush(q, (alt, c, v))
                dist[v] = alt
                c += 1

    return dist[dst]


def lowest_loss(map: list[list[int]]) -> int:
    """Compute lowest heat loss."""
    srcs = []
    dsts = []
    for d in [Direction.U, Direction.D, Direction.L, Direction.R]:
        srcs.append(Vertex(0, 0, d, 0))

    for d in [Direction.U, Direction.D, Direction.L, Direction.R]:
        for s in range(4, 11):
            dsts.append(Vertex(len(map) - 1, len(map[0]) - 1, d, s))

    return min(
        distance(map, src, dst) for src, dst in tqdm(itertools.product(srcs, dsts))
    )


def solve(path: Path) -> None:
    """Solve the puzzle."""
    map = read_map(path)

    loss = lowest_loss(map)
    print(loss)


def main() -> int:
    path = parse_arguments()
    solve(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
