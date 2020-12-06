# Advent of Code 2020, Day 6, Part 1
# Author: Bobby Nelson

def read_file(filename):
    with open(filename) as file:
        return file.readlines()

def line_sum(line):
    return len(set(line))

def group_sum(line_list):
    line_list.extend("\n")
    count = 0
    group = []
    for line in line_list:
        line = line.rstrip("\n")
        if line == "":
            count += line_sum(group)
            group = []
        else:
            group.extend(list(line))
            
    return count
    
if __name__ == "__main__":
    input = read_file("input.txt")
    print(f"Part 1: {group_sum(input)}")
