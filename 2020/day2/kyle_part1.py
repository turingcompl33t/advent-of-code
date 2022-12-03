# kyle_part1.py
#
# Advent of Code Day 2 Puzzle 1.

FILENAME = "input.txt"

# lazily yield lines from the input file
def lines() -> str:
    with open(FILENAME, "r") as f:
        for line in f:
            yield line.strip()

# determine if the given line contains a 
# password that satisfies corporate policy
def satisfies_policy(line: str) -> bool:
    policy, target = map(str.strip, line.split(":"))
    range, char = policy.split()
    min_count, max_count = map(int, range.split("-"))
    count = target.count(char)
    return (count >= min_count) and (count <= max_count)

def main():
    s = sum([satisfies_policy(l) for l in lines()])
    print(f"{s}")

if __name__ == "__main__":
    main()