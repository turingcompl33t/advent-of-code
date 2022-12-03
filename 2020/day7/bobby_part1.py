# Advent of Code 2020, Day 7, Part 1
# Author: Bobby Nelson

import re

def read_file(filename):
    with open(filename) as file:
        return file.readlines()

def parse_rule(rule):
    outer_bag = re.search(r'(.*) bags contain', rule).group(1)
    inner_bag_list = re.findall(r'\d+ (.*?) bag', rule)
    return (outer_bag, inner_bag_list)

def check_contains(bag_dict, current_color, search_color):
    if search_color in bag_dict[current_color]:
        return 1
    elif not bag_dict[current_color]:
        # Empty bag
        return 0
    else:
        for color in bag_dict[current_color]:
            if check_contains(bag_dict, color, search_color):
                return 1
        return 0

def calc_bags(rule_list, bag_color):
    bag_dict = dict((parse_rule(rule) for rule in rule_list))

    count = 0
    for bag in bag_dict.keys():
        count += check_contains(bag_dict, bag, bag_color)
    return count
    
if __name__ == "__main__":
    input = read_file("input.txt")
    bag_color = "shiny gold"
    print(f"Part 1: {calc_bags(input, bag_color)}")
