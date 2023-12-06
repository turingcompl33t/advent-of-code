"""
part3.py

Advent of Code 2023, Day 5, Part 2 (reprise).
"""

from __future__ import annotations

import sys
from tqdm import tqdm
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

    def lookup(self, src_val: int) -> int:
        """Compute the desintation value for a source value."""
        for entry in self.map:
            if src_val in range(entry.src_begin, entry.src_begin + entry.length):
                return entry.dst_begin + (src_val - entry.src_begin)

        return src_val

    def reverse_lookup(self, dst_val: int) -> int:
        """Compute the source value for a destination value."""
        for entry in self.map:
            if dst_val in range(entry.dst_begin, entry.dst_begin + entry.length):
                return entry.src_begin + (dst_val - entry.dst_begin)

        return dst_val

    @staticmethod
    def parse(string: str) -> Map:
        """Parse a map from a string."""
        string = string.strip("\n")

        name_line, *rest = string.split("\n")

        map_name = name_line.split()[0]
        src, _, dst = map_name.split("-")

        return Map(src=src, dst=dst, map=[MapEntry.parse(line) for line in rest])


class SeedRange:
    """Represents a range of seeds."""

    def __init__(self, *, begin: int, length: int) -> None:
        self.begin = begin
        """The beginning seed number."""

        self.length = length
        """The length of the range."""

    def contains(self, seed: int) -> bool:
        """Determine if the range contains the given seed."""
        return seed >= self.begin and seed < self.begin + self.length

    def __str__(self) -> str:
        return f"SeedRange(begin={self.begin}, length={self.length})"


def parse_seeds(chunk: str) -> list[SeedRange]:
    """Parse seeds from a chunk."""
    _, seed_numbers = chunk.strip("\n").split(":")
    seed_numbers = seed_numbers.split()

    ranges = []
    for i in range(0, len(seed_numbers), 2):
        ranges.append(
            SeedRange(begin=int(seed_numbers[i]), length=int(seed_numbers[i + 1]))
        )

    return ranges


def find_map(dst: str, maps: list[Map]) -> Map:
    """Find the appropriate map to use."""
    for map in maps:
        if map.dst == dst:
            return map

    raise RuntimeError(f"map for destination {dst} not found")


def compute_seed_for_location_number(location_number: int, maps: list[Map]) -> int:
    """Compute the seed value for a given location number."""
    # The current mapping location
    val = location_number
    dst = "location"

    while dst != "seed":
        m = find_map(dst, maps)

        val = m.reverse_lookup(val)
        dst = m.src

    return val


def infinity() -> int:
    """Yield all values in [0, infinity)."""
    i = 0
    while True:
        yield i
        i = i + 1


def solve(path: Path) -> None:
    """Solve the puzzle."""
    chunks = read_chunks(path)

    seed_ranges = parse_seeds(chunks[0])

    maps = [Map.parse(chunk) for chunk in chunks[1:]]

    for location_number in infinity():
        seed = compute_seed_for_location_number(location_number, maps)
        for range in seed_ranges:
            if range.contains(seed):
                print(location_number)
                return


def main() -> int:
    path = parse_arguments()
    solve(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
