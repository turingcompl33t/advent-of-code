# Advent of Code 2020, Day 7, Part 2
# Author: Bobby Nelson

import re

def read_file(filename):
    with open(filename) as file:
        return file.readlines()

def parse_rule(rule):
    outer_bag = re.search(r'(.*) bags contain', rule).group(1)
    inner_bag_list = re.findall(r'(\d+) (.*?) bag', rule)
    return (outer_bag, inner_bag_list)

def check_contains(bag_dict, current_color):
    total = 1
    for num, bag in bag_dict[current_color]:
        total += int(num) * check_contains(bag_dict, bag)
    return total

def calc_bags(rule_list, bag_color):
    bag_dict = dict((parse_rule(rule) for rule in rule_list))

    count = 0
    for bag in bag_dict.keys():
        if bag == bag_color:
            count += check_contains(bag_dict, bag)

    return count-1
    
if __name__ == "__main__":
    input = read_file("input.txt")
    bag_color = "shiny gold"
    print(f"Part 2: {calc_bags(input, bag_color)}")
