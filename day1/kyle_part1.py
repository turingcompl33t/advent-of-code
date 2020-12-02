# kyle_part1.py
#
# Advent of Code Day 1 Part 1.

from typing import List, Tuple

FILENAME = "input.txt"

# read values from input file
def read_values() -> List[int]:
    with open(FILENAME, "r") as f:
        return [int(v) for v in f.readlines()]

# lazy cartesian product coroutine
def cartesian_product(values: List[int]) -> Tuple[int, int]:
    for a in values:
        for b in values:
            yield (a, b)

def main():
    for first, second in cartesian_product(read_values()):
        if first + second == 2020:
            print(f"Values:  ({first}, {second})")
            print(f"Product: {first*second}")
            break

if __name__ == "__main__":
    main()