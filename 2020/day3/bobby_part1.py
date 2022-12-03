# Advent of Code 2020, Day 3, Part 1
# Author: Bobby Nelson

def read_file(filename):
    with open(filename) as file:
        return [list(line.rstrip('\n')) for line in file]

def calculate_trees(coordinates):
    h_slope = 3 # move right 3 times
    v_slope = 1 # move down 1 time
    width = len(coordinates[0])
    h_pos = 0
    v_pos = 0
    tree_counter = 0
    while (v_pos < len(coordinates)):
        if coordinates[v_pos][h_pos % width] == '#':
            tree_counter += 1
        h_pos += h_slope
        v_pos += v_slope
    return tree_counter
    

if __name__ == "__main__":
    input = read_file("input.txt")
    print(calculate_trees(input))
