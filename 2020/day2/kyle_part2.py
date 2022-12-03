# kyle_part2.py
#
# Advent of Code Day 2 Puzzle 2.

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
    indices, char = policy.split()
    lower, upper = map(int, indices.split("-"))
    return sum([target[lower - 1] is char, target[upper - 1] is char]) is 1

def main():
    s = sum([satisfies_policy(l) for l in lines()])
    print(f"{s}")

if __name__ == "__main__":
    main()