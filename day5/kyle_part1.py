# kyle_part1.py
#
# Advent of Code Day 5 Puzzle 1.

LOWER = frozenset(["L", "F"])
UPPER = frozenset(["R", "B"])

FILENAME = "input.txt"

def lines() -> str:
    with open(FILENAME, "r") as f:
        for line in f:
            yield line.strip()

def binary_search(line: str, lower: int, upper: int) -> int:
    if (upper - lower) <= 1:
        return lower if line in LOWER else upper
    return binary_search(line[1:], lower, (lower + upper) // 2) if line[0] in LOWER\
         else binary_search(line[1:], ((lower + upper) // 2) + 1, upper)

def to_id(line: str) -> int:
    return binary_search(line[:7], 0, 127)*8 + binary_search(line[7:], 0, 7)

def main():
    m = max([to_id(line) for line in lines()])
    print(f"Maximum seat ID: {m}")

if __name__ == "__main__":
    main()