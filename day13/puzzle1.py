# kyle_part1.py
#
# Advent of Code Day 13 Puzzle 1.

from typing import Tuple, List

FILENAME = "input.txt"

def read_input() -> Tuple[int, List[int]]:
    with open(FILENAME, "r") as f:
        lines = f.readlines()
        return (int(lines[0]), [int(n) for n in lines[1].split(",") if n != "x"])

def lowest_multiple_above(x: int, n: int) -> int:
    return (n // x)*x + x

def main():
    earliest_ts, bus_ids = read_input()
    z = zip(bus_ids, [lowest_multiple_above(x, earliest_ts) for x in bus_ids])
    z = min(z, key=lambda x: x[1])
    z = (z[1] - earliest_ts) * z[0]

    print(f"Value: {z}")

if __name__ == "__main__":
    main()