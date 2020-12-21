# kyle_part2.py
#
# Advent of Code Day 13 Puzzle 2.

import functools
from typing import List, Tuple

FILENAME = "input.txt"

def read_bus_ids() -> List[Tuple[int, int]]:
    with open(FILENAME, "r") as f:
        _ = f.readline()
        return [(i, int(x)) for i, x in enumerate(f.readline().split(",")) if x != "x"]

def product(iterable) -> int:
    return functools.reduce(lambda x, y: x*y, iterable, 1)

def eea(a: int, b: int) -> Tuple[int, int, int]:
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_s, old_t, old_r

def crt(rem: List[int], div: List[int]) -> int:
    M = product(div)
    a = list(map(lambda d: int(M / d), div))
    r = map(lambda t: eea(*t), zip(a, div))
    i = [res[0] % d for res, d in zip(r, div)]
    Z = sum(map(product, zip(i, rem, a)))
    return Z % M

def main():
    bus_ids = read_bus_ids()

    r = [(-b[0] % b[1]) for b in bus_ids]
    d = [b[1] for b in bus_ids]
    print(f"First occurence at timestamp: {crt(r, d)}")
        
if __name__ == "__main__":
    main()