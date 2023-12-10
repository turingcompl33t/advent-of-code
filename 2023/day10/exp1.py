"""
exp1.py

Advent of Code 2023, Day 10, Part 1 experimentation.
"""

from __future__ import annotations

import sys
import argparse
from tqdm import tqdm
from enum import Enum
from pathlib import Path
from typing import Optional
from collections import OrderedDict

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

    def indices_of(self, tile: Tile) -> list[tuple[int, int]]:
        """Get indices for specified tile type."""
        tiles = []
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[i])):
                if self.tiles[i][j] == tile:
                    tiles.append((i, j))
        return tiles

    def start_index(self) -> tuple[int, int]:
        """Get the index of the start tile."""
        start = self.indices_of(Tile.START)
        assert len(start) == 1, "Must have a single start tile."
        return start[0]


def adjacent_above(maze: Maze, i: int, j: int) -> Optional[tuple[int, int]]:
    """Determine the adjacent above."""
    if i == 0:
        return None

    above = maze.tiles[i - 1][j]
    if above == Tile.VERTICAL_PIPE or above == Tile.BEND_SE or above == Tile.BEND_SW:
        return (i - 1, j)

    return None


def adjacent_below(maze: Maze, i: int, j: int) -> Optional[tuple[int, int]]:
    """Determine adjacent below."""
    if i >= (len(maze.tiles) - 1):
        return None

    below = maze.tiles[i + 1][j]
    if below == Tile.VERTICAL_PIPE or below == Tile.BEND_NE or below == Tile.BEND_NW:
        return (i + 1, j)

    return None


def adjacent_left(maze: Maze, i: int, j: int) -> Optional[tuple[int, int]]:
    """Determine adjacent left."""
    if j == 0:
        return None

    left = maze.tiles[i][j - 1]
    if left == Tile.HORIZONTAL_PIPE or left == Tile.BEND_NE or left == Tile.BEND_SE:
        return (i, j - 1)

    return None


def adjacent_right(maze: Maze, i: int, j: int) -> Optional[tuple[int, int]]:
    """Determine adjacent right."""
    if j >= (len(maze.tiles[i]) - 1):
        return None

    right = maze.tiles[i][j + 1]
    if right == Tile.HORIZONTAL_PIPE or right == Tile.BEND_NW or right == Tile.BEND_SW:
        return (i, j + 1)

    return None


class Graph:
    """A generic graph."""

    def __init__(self) -> None:
        self._vertices: OrderedDict[
            tuple[int, int], list[tuple[tuple[int, int], int]]
        ] = OrderedDict()
        """Adjacency list."""

    def add_vertex(self, v: tuple[int, int]) -> None:
        """Add a vertex."""
        if v in self._vertices:
            raise RuntimeError("cannot add duplicate vertex")
        self._vertices[v] = []

    def add_edge(
        self, src: tuple[int, int], dst: tuple[int, int], weight: int = 1
    ) -> None:
        """Add an edge."""
        if src not in self._vertices:
            raise RuntimeError("missing vertex")
        if dst not in self._vertices:
            raise RuntimeError("missing vertex")

        self._vertices[src].append((dst, weight))

    @property
    def vertices(self) -> list[tuple[int, int]]:
        """Return a list of the vertex identifiers."""
        return [key for key in self._vertices.keys()]

    @property
    def edges(self) -> list[tuple[tuple[int, int], tuple[int, int], int]]:
        """Return a list of the edge identifiers."""
        edges = []
        for src in self._vertices.keys():
            edges.extend([(src, dst, weight) for dst, weight in self._vertices[src]])
        return edges

    def index_of(self, v: tuple[int, int]) -> int:
        """Get the index of the given vertex identifier."""
        if v not in self._vertices:
            raise KeyError(f"Vertex {v} does not exist.")
        for index, key in enumerate(self._vertices):
            if key == v:
                return index
        assert False, "Unreachable."

    def at_index(self, index: int) -> tuple[int, int]:
        """Get the vertex ID for the vertex at index `index`."""
        if index >= len(self._vertices):
            raise IndexError("Out of range.")
        for i, vertex in enumerate(self._vertices.keys()):
            if i == index:
                return vertex
        assert False, "Unreachable."

    def adjacent(self, v: tuple[str, str]) -> list[tuple[tuple[int, int], int]]:
        """Return the vertices that are adjacent to `vertex_id`."""
        if v not in self._vertices:
            raise KeyError(f"Vertex {v} does not exist.")
        return [(id, weight) for id, weight in self._vertices[v]]


def build_graph(maze: Maze) -> Graph:
    """Build a maze from a graph."""
    g = Graph()
    for row in range(len(maze.tiles)):
        for col in range(len(maze.tiles[row])):
            neighbors = maze.adjacent(row, col)

            if (row, col) not in g.vertices:
                g.add_vertex((row, col))

            for n_row, n_col in neighbors:
                if (n_row, n_col) not in g.vertices:
                    g.add_vertex((n_row, n_col))

                g.add_edge((row, col), (n_row, n_col))

    return g


def floyd_warshall(g: Graph) -> Graph:
    """Run floyd-warshall to compute all-pairs shortest paths."""
    # Translate the graph to an adjacency matrix formulation
    n_vertices = len(g.vertices)

    # |V| x |V| matrix representing the path cost between all vertex pairs
    matrix = [[INF for _ in range(n_vertices)] for _ in range(n_vertices)]

    # Initialize path weights for adjacent vertices
    for src, dst, _ in g.edges:
        matrix[g.index_of(src)][g.index_of(dst)] = 1

    # Initialize path weights for vertex -> self
    for vertex in g.vertices:
        matrix[g.index_of(vertex)][g.index_of(vertex)] = 0

    # Execute path-finding procedure
    pbar = tqdm(total=n_vertices * n_vertices * n_vertices)
    for k in range(n_vertices):
        for i in range(n_vertices):
            for j in range(n_vertices):
                if matrix[i][j] > matrix[i][k] + matrix[k][j]:
                    matrix[i][j] = matrix[i][k] + matrix[k][j]
                pbar.update(1)

    # Reconstruct the output graph
    g_star = Graph()
    for vertex in g.vertices:
        g_star.add_vertex(vertex)

    for i in range(n_vertices):
        for j in range(n_vertices):
            src = g.at_index(i)
            dst = g.at_index(j)
            weight = matrix[i][j]

            g_star.add_edge(src, dst, weight)

    return g_star


def solve(path: Path) -> None:
    """Solve the puzzle."""
    with path.open("r") as f:
        lines = f.readlines()

    # Parse the maze
    maze = Maze.parse([line.strip() for line in lines])

    # Build a graph from the maze
    g = build_graph(maze)

    # Compute a distance graph with floyd-warshall
    d = floyd_warshall(g)

    # Compute candidates
    candidates = [
        (t, weight) for (t, weight) in d.adjacent(maze.start_index()) if weight != INF
    ]

    # Compute maximum distance
    dist = max(weight for _, weight in candidates)
    print(dist)


def main() -> int:
    path = parse_arguments()
    solve(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
