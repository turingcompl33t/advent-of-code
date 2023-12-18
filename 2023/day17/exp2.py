"""
exp2.py
"""

import sys
import heapq
from collections import namedtuple
from enum import Enum

class Direction(Enum):
    R = "r"
    L = "l"

Vertex = namedtuple("Vertex", "i j d s")

def main() -> int:
    q = [(0, Vertex(0, 0, Direction.R, 0))]

    _, v = heapq.heappop(q)
    print(v)

    return 0

if __name__ == "__main__":
    sys.exit(main())