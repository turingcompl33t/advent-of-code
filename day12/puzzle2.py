# kyle_part2.py
#
# Advent of Code Day 12 Puzzle 2.

import math
from typing import Tuple

FILENAME = "input.txt"

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

def lines() -> str:
    with open(FILENAME, "r") as f:
        for line in f:
            yield line.strip()

def rotate_point(p: Point, angle: int) -> Point:
    # assumes counter-clockwise turns only
    if 90 == angle:
        return Point(-p.y, p.x)
    if 180 == angle:
        return Point(-p.x, -p.y)
    if 270 == angle:
        return Point(p.y, -p.x)

def process_line(line: str, ship: Point, waypoint: Point) -> Tuple[Point, Point]:
    if line[0] == "N":
        return (ship, Point(waypoint.x, waypoint.y + int(line[1:])))
    if line[0] == "E":
        return (ship, Point(waypoint.x + int(line[1:]), waypoint.y))
    if line[0] == "S":
        return (ship, Point(waypoint.x, waypoint.y - int(line[1:])))
    if line[0] == "W":
        return (ship, Point(waypoint.x - int(line[1:]), waypoint.y))
    if line[0] == "F":
        dt = int(line[1:])
        dx = waypoint.x*dt
        dy = waypoint.y*dt
        return (Point(ship.x + dx, ship.y + dy), waypoint)
    if line[0] == "L":
        return (ship, rotate_point(waypoint, int(line[1:])))
    if line[0] == "R":
        return (ship, rotate_point(waypoint, 360 - int(line[1:])))

def main():
    ship     = Point(0, 0)
    waypoint = Point(10, 1)
    for line in lines():
        ship, waypoint = process_line(line, ship, waypoint)

    c = sum(map(abs, [ship.x, ship.y]))
    print(f"Final distance: {c}")

if __name__ == "__main__":
    main()