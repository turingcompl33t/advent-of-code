"""
part1.py

Advent of Code 2023, Day 8, Part 2 (reprise).
"""

from __future__ import annotations

import sys
import math
import argparse
from pathlib import Path
from enum import Enum

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def parse_arguments() -> Path:
    """Parse commandline arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, help="The path to the input file.")
    args = parser.parse_args()
    return args.path


class Instruction(Enum):
    """An instruction from the document."""

    LEFT = "left"
    RIGHT = "right"

    @staticmethod
    def parse(string: str) -> Instruction:
        """Parse an instruction from a sting."""
        match string:
            case "L":
                return Instruction.LEFT
            case "R":
                return Instruction.RIGHT
            case _:
                raise RuntimeError(f"invaid instruction '{string}'")

    def __str__(self) -> str:
        return f"Instruction({self.value})"


def parse_node(string: str) -> tuple[str, str, str]:
    """Parse a node from a string."""
    name, rest = string.split("=")
    l, r = rest.split(",")
    return name.strip(), l.strip("( "), r.strip(" )")


def parse(path: Path) -> tuple[list[Instruction], dict[str, dict[Instruction, str]]]:
    """
    Parse instructions and nodes from the input file.
    """
    with path.open("r") as f:
        lines = f.readlines()

    instrs = [Instruction.parse(c) for c in lines[0].strip()]

    name, l, r = parse_node(lines[2].strip())

    nodes: dict[str, dict[Instruction, str]] = {}
    for line in lines[2:]:
        name, l, r = parse_node(line.strip())
        if name in nodes:
            raise RuntimeError(f"duplicate node '{name}'")

        nodes[name] = {Instruction.LEFT: l, Instruction.RIGHT: r}

    return instrs, nodes


def infinity() -> int:
    """An infinite sequence."""
    i = 0
    while True:
        yield i
        i = i + 1


def solve_for_start_location(
    name: str, instrs: list[Instruction], nodes: dict[str, dict[Instruction, str]]
) -> int:
    """Solve the problem for a single start location."""
    location = name
    for step in infinity():
        if location.endswith("Z"):
            return step

        # Find the next instruction
        instr = instrs[step % len(instrs)]
        # Apply the instruction
        location = nodes[location][instr]


def solve(path: Path) -> None:
    """Solve the puzzle."""
    instrs, nodes = parse(path)

    # All starting locations
    locations = [name for name in nodes.keys() if name.endswith("A")]
    multiples = [solve_for_start_location(loc, instrs, nodes) for loc in locations]

    steps = math.lcm(*multiples)
    print(steps)


def main() -> int:
    path = parse_arguments()
    solve(path)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
