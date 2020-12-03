# kyle_part1.py
#
# Advent of Code Day 3 Puzzle 1.

import operator
import functools
import itertools

FILENAME = "input.txt"

def lines() -> str:
    with open(FILENAME, "r") as f:
        for line in f:
            yield line.strip()

def hits_for_slope(right: int, down: int) -> int:
    # perhaps not the most readable way to express this...
    # but I'll be damned if Robin can implement this more concisely in elixir
    return sum([line[(i*right)%len(line)] == "#" for i, line in enumerate(itertools.islice(lines(), 0, None, down))])

def main():
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    s = functools.reduce(operator.mul, [hits_for_slope(*s) for s in slopes])
    print(f"Product of hits on all slopes: {s} trees, mega-ouch")

if __name__ == "__main__":
    main()