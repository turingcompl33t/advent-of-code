# Advent of Code 2020, Day 3, Part 2
# Author: Bobby Nelson

def read_file(filename):
    with open(filename) as file:
        return [list(line.rstrip('\n')) for line in file]

def calculate_trees(coordinates, h_slope, v_slope):
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
    h_slopes = [1, 3, 5, 7, 1]
    v_slopes = [1, 1, 1, 1, 2]
    answer = 1
    for i in range(0, len(h_slopes)):
        answer = answer * calculate_trees(input, h_slopes[i], v_slopes[i])
    print(answer)
