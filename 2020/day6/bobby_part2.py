# Advent of Code 2020, Day 6, Part 2
# Author: Bobby Nelson

def read_file(filename):
    with open(filename) as file:
        return file.readlines()

def group_sum(group):
    return len(set.intersection(*group))

def total_sum(line_list):
    line_list.extend("\n")
    count = 0
    group = []
    for line in line_list:
        line = line.rstrip("\n")
        if line == "":
            count += group_sum(group)
            group = []
        else:
            group.append(set(line))
            
    return count
    
if __name__ == "__main__":
    input = read_file("input.txt")
    print(f"Part 2: {total_sum(input)}")
