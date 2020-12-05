# kyle_part1.py
#
# Advent of Code Day 4 Puzzle 1.

from typing import FrozenSet

FILENAME = "input.txt"

def chunks():
    with open(FILENAME, "r") as f:
        data = f.read()
        chunks = data.split("\n\n")
        for chunk in chunks:
            yield " ".join(chunk.split("\n"))

def keys(chunk: str) -> FrozenSet[str]:
    return frozenset([kv.split(":")[0] for kv in chunk.split()])

def intersection_cardinality(s1: FrozenSet[str], s2: FrozenSet[str]) -> int:
    return len(s1.intersection(s2))

def main():
    r = frozenset(["byr", "iyr", "eyr", "hgt", "hcl", "ecl",  "pid"])
    s = sum([intersection_cardinality(keys(c), r) == len(r) for c in chunks()])
    print(f"{s} valid passports")

if __name__ == "__main__":
    main()