# Advent of Code 2020, Day 2, Part 2
# Author: Bobby Nelson

def read_file(filename):
    with open(filename) as file:
        return [line.rstrip('\n') for line in file]

def check_passwords(pwd_list):
    counter = 0
    for line in pwd_list:
        rule, password = [x.strip() for x in line.split(':')]
        positions, letter = rule.split()
        pos_one, pos_two = [int(x)-1 for x in positions.split('-')]
        if (password[pos_one] == letter) != (password[pos_two] == letter):
            counter = counter + 1
    return counter

if __name__ == "__main__":
    input = read_file("input.txt")
    print(check_passwords(input))
