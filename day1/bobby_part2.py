# Advent of Code 2020, Day 1, Part 2
# Author: Bobby Nelson

from itertools import combinations

def read_file(filename):
    with open(filename) as f:
        return [int(x) for x in f]

def calculate(list):
    comb = combinations(list, 3)
    for x in comb:
        if sum(x) == 2020:
            return x[0] * x[1] * x[2]
    
if __name__ == "__main__":
    input = read_file("input")
    print(calculate(input))
