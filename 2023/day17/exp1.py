"""
part1.py

Advent of Code 2023, Day 17, Part 2.
"""

from __future__ import annotations

import sys
import argparse
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


Point = namedtuple("Point", "i j")


class Direction(Enum):
    """An enumeration over directions."""

    U = "up"
    D = "down"
    L = "left"
    R = "right"


class Graph:
    """A graph abstraction."""

    def __init__(self) -> None:
        self.vertices: dict[Point, dict[Point, tuple[Direction, int]]] = {}
        """The underlying adjacency list."""

    def add_vertex(self, p: Point) -> None:
        """Add a vertex to the graph."""
        if p in self.vertices:
            raise RuntimeError(f"duplicate vertex {p}")
        self.vertices[p] = {}

    def add_edge(self, a: Point, b: Point, d: Direction, w: int) -> None:
        """Add an edge to a graph."""
        if a not in self.vertices:
            raise RuntimeError(f"{a} not in graph")
        if b not in self.vertices:
            raise RuntimeError(f"{b} not in graph")

        if b in self.vertices[a]:
            raise RuntimeError(f"edge {a} -> {b} not in graph")

        self.vertices[a][b] = (d, w)

    def edge(self, a: Point, b: Point) -> tuple[Direction, int]:
        """Get the edge from a to b."""
        if a not in self.vertices:
            raise RuntimeError(f"{a} not in graph")
        if b not in self.vertices[a]:
            raise RuntimeError(f"edge {a} -> {b} not in graph")
        return self.vertices[a][b]

    def adjacent(self, p: Point) -> dict[Point, tuple[Direction, int]]:
        """Get adjacent vertices for a point."""
        if p not in self.vertices:
            raise RuntimeError(f"{p} not in graph")
        return self.vertices[p]

def up(map: list[list[int]], p: Point) -> Optional[Point]:
    """Return the point in the Up direction."""
    return Point(p.i - 1, p.j) if p.i - 1 >= 0 else None


def down(map: list[list[str]], p: Point) -> Optional[Point]:
    """Return the point in the Down direction."""
    return Point(p.i + 1, p.j) if p.i + 1 < len(map) else None


def left(map: list[list[str]], p: Point) -> Optional[Point]:
    """Return the point in the Left direction."""
    return Point(p.i, p.j - 1) if p.j - 1 >= 0 else None


def right(map: list[list[int]], p: Point) -> Optional[Point]:
    """Return the point in the Right direction."""
    return Point(p.i, p.j + 1) if p.j + 1 < len(map[0]) else None


def build_graph(map: list[list[int]]) -> Graph:
    """Build a graph from the map."""
    g = Graph()
    for i in range(len(map)):
        for j in range(len(map[0])):
            p = Point(i, j)
            if p not in g.vertices:
                g.add_vertex(p)

            u = up(map, p)
            if u is not None:
                if u not in g.vertices:
                    g.add_vertex(u)
                g.add_edge(p, u, Direction.U, map[u.i][u.j])

            d = down(map, p)
            if d is not None:
                if d not in g.vertices:
                    g.add_vertex(d)
                g.add_edge(p, d, Direction.D, map[d.i][d.j])

            l = left(map, p)
            if l is not None:
                if l not in g.vertices:
                    g.add_vertex(l)
                g.add_edge(p, l, Direction.L, map[l.i][l.j])

            r = right(map, p)
            if r is not None:
                if r not in g.vertices:
                    g.add_vertex(r)
                g.add_edge(p, r, Direction.R, map[r.i][r.j])

    return g

def pop_min(q: list[Point], dist: dict[Point, int]) -> Point:
    """Pop the point with minimum distance."""
    mind = INF
    mini = -1
    for i, p in enumerate(q):
        if dist[p] < mind:
            mind = dist[p]
            mini = i
    return q.pop(mini)

def prev3(p: Point, prev: dict[Point, Point]) -> None:
    """Get the previous three directions for a point."""
    pass

def dijkstra(g: Graph, start: Point, goal: Point) -> None:
    """Run Dijkstra's algorithm to find shortest path to goal."""
    dist: dict[Point, int] = {}
    prev: dict[Point,  Point] = {}
    
    q: list[Point] = []
    for v in g.vertices.keys():
        dist[v] = INF
        prev[v] = Point(-1, -1)
        q.append(v)

    dist[start] = 0

    while len(q) > 0:
        u = pop_min(q, dist)

        adjacent = g.adjacent(u)
        for v, (d, w) in adjacent.items():
            if v not in q:
                continue
            alt = dist[u] + w
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u

def solve(path: Path) -> None:
    """Solve the puzzle."""
    g = build_graph(read_map(path))

    # Compute start and goal vertices
    start = Point(0, 0)
    goal = Point(len(map) - 1, len(map[0]) - 1)


def main() -> int:
    path = parse_arguments()
    solve(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
