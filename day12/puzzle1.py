# kyle_part1.py
#
# Advent of Code Day 12 Puzzle 1.

FILENAME = "input.txt"

DIRECTION_TO_HEADING = {"E": 0, "N": 90, "W": 180, "S": 270}
HEADING_TO_DIRECTION = {0: "E", 90: "N", 180: "W", 270: "S"}

def lines():
    with open(FILENAME, "r") as f:
        for line in f:
            yield line.strip()

def new_direction(current, token):
    if not ((token[0] == "R") or (token[0] == "L")):
        return current 
    diff = int(token[1:]) if token[0] == "L" else 360 - int(token[1:])
    return HEADING_TO_DIRECTION[(DIRECTION_TO_HEADING[current] + (diff % 360)) % 360]

def new_position(current, token, direction):
    x, y = current
    if token[0] == "N" or (token[0] == "F" and direction == "N"):
        return (x, y + int(token[1:]))
    if token[0] == "E" or (token[0] == "F" and direction == "E"):
        return (x + int(token[1:]), y)
    if token[0] == "S" or (token[0] == "F" and direction == "S"):
        return (x, y - int(token[1:]))
    if token[0] == "W" or (token[0] == "F" and direction == "W"):
        return (x - int(token[1:]), y)
    return (x, y)

def exclusive_scan(init, src, update):
    dst = [init]
    for i in range(len(src) - 1):
        dst.append(update((dst[i], src[i])))
    return dst

def inclusive_scan(init, src, update):
    dst = [init]
    for i in range(len(src)):
        dst.append(update((dst[i], src[i])))
    return dst 

def main():
    l = [line for line in lines()]
    directions = list(zip(l, exclusive_scan("E", l, lambda x: new_direction(x[0], x[1]))))
    positions  = inclusive_scan((0, 0), directions, lambda x: new_position(x[0], x[1][0], x[1][1]))

    distance = sum(map(abs, positions[-1]))
    print(f"Final distance: {distance}")

if __name__ == "__main__":
    main()