# setup.py
#
# Setup directory structure.

import os
import shutil

# total number of puzzles in Advent of Code 2020
N_DAYS = 25

def main():
    for i in range(1, N_DAYS + 1):
        dir = f"day{i}"
        if not os.path.exists(dir):
            os.mkdir(dir)
            path = os.path.join(dir, "placeholder.txt")
            with open(path, "w") as f:
                f.write("placeholder")

if __name__ == "__main__":
    main()