# Advent of Code 2020, Day 2, Part 1
# Author: Bobby Nelson

def read_file(filename):
    with open(filename) as file:
        return [line.rstrip('\n') for line in file]

def check_passwords(pwd_list):
    counter = 0
    for line in pwd_list:
        rule, password = line.split(':')
        ranges, letter = rule.split()
        min, max = [int(x) for x in ranges.split('-')]
        if (password.count(letter) >= min) and (password.count(letter) <= max):
            counter = counter + 1
    return counter

if __name__ == "__main__":
    input = read_file("input.txt")
    print(check_passwords(input))
