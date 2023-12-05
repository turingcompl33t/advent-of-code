"""
part1.py

Advent of Code 2023, Day 5, Part 1.
"""

from __future__ import annotations

import sys
import argparse
from pathlib import Path

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def parse_arguments() -> Path:
    """Parse commandline arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, help="The path to the input file.")
    args = parser.parse_args()
    return args.path


def read_chunks(path: Path) -> list[str]:
    """Read chunks from a file."""
    chunks = []
    with path.open("r") as f:
        chunk = ""
        for line in f:
            if line == "\n":
                chunks.append(chunk)
                chunk = ""
            else:
                chunk += line
    
    chunks.append(chunk)
    return chunks


class MapEntry:
    """A map entry."""

    def __init__(self, *, src_begin: int, dst_begin: int, length: int) -> None:
        self.src_begin = src_begin
        """The source begin value."""

        self.dst_begin = dst_begin
        """The desintation begin value."""

        self.length = length
        """The range length."""

    @staticmethod
    def parse(string: str) -> MapEntry:
        """Parse a map entry from a string."""
        dst_begin, src_begin, length = string.split()
        return MapEntry(
            src_begin=int(src_begin), dst_begin=int(dst_begin), length=int(length)
        )
    
    def __str__(self) -> str:
        return f"MapEntry(src={self.src_begin}, dst={self.dst_begin}, length={self.length})"


class Map:
    """A parsed map."""

    def __init__(self, *, src: str, dst: str, map: list[MapEntry]) -> None:
        self.src = src
        """The source name."""

        self.dst = dst
        """The destination name."""

        self.map = map
        """The underlying map."""

    def value_for(self, src_val: int) -> int:
        """Compute the corresponding value for an input value."""
        for entry in self.map:
            if src_val in range(entry.src_begin, entry.src_begin + entry.length):
                return entry.dst_begin + (src_val - entry.src_begin)
            
        return src_val

    @staticmethod
    def parse(string: str) -> Map:
        """Parse a map from a string."""
        string = string.strip("\n")

        name_line, *rest = string.split("\n")

        map_name = name_line.split()[0]
        src, _, dst = map_name.split("-")

        return Map(src=src, dst=dst, map=[MapEntry.parse(line) for line in rest])


def parse_seeds(chunk: str) -> list[int]:
    """Parse seeds from a chunk."""
    _, seed_numbers = chunk.strip("\n").split(":")
    return [int(n) for n in seed_numbers.split()]

def find_map(src: str, maps: list[Map]) -> Map:
    """Find the appropriate map to use."""
    for map in maps:
        if map.src == src:
            return map
    
    raise RuntimeError(f"map for source {src} not found")

def compute_location_number_for_seed(seed: int, maps: list[Map]) -> int:
    """Compute the location number for a given seed."""
    # The current mapping location
    val = seed
    src = "seed"

    while src != "location":
        m = find_map(src, maps)
        
        # Transition to the new mapping location
        val = m.value_for(val)
        src = m.dst

    return val

def solve(path: Path) -> None:
    """Solve the puzzle."""
    chunks = read_chunks(path)

    seeds = parse_seeds(chunks[0])

    maps = [Map.parse(chunk) for chunk in chunks[1:]]

    min_loc = min(compute_location_number_for_seed(seed, maps) for seed in seeds)
    print(min_loc)


def main() -> int:
    path = parse_arguments()
    solve(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
