# kyle_part1.py
#
# Advent of Code Day 3 Puzzle 1.

FILENAME = "input.txt"

def lines() -> str:
    with open(FILENAME, "r") as f:
        for line in f:
            yield line.strip()

def main():
    s = sum([line[(i*3)%len(line)] == "#" for i, line in enumerate(lines())])
    print(f"Hit {s} trees, ouch")

if __name__ == "__main__":
    main()