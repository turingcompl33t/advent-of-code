# kyle_part2.py
#
# Advent of Code Day 1 Part 2.

from typing import List, Tuple

FILENAME = "input.txt"

# read values from input file
def read_values() -> List[int]:
    with open(FILENAME, "r") as f:
        return [int(v) for v in f.readlines()]

# lazy triple product
# NOTE: must be a clean generalization 
# of an n-way cartesian product...
def triple_product(values: List[int]) -> Tuple[int, int, int]:
    for a in values:
        for b in values:
            for c in values:
                yield (a, b, c)

def main():
    for first, second, third in triple_product(read_values()):
        if (first + second + third) == 2020:
            print(f"Values:  ({first}, {second}, {third})")
            print(f"Product: {first*second*third}")
            break

if __name__ == "__main__":
    main()