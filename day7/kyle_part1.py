# kyle_part1.py
#
# Advent of Code Day 7 Puzzle 1.

import re
from typing import List, Dict, Tuple

FILENAME = "input.txt"

def lines() -> str:
    with open(FILENAME, "r") as f:
        for line in f:
            yield line.strip()

def parse_line(line: str) -> Tuple[str, List[str]]:
    s = line.split("contain")
    key, vals = [p.strip() for p in s]
    key = re.sub("bags\s*$", "", key).strip()
    if "no other bags." == vals:
        vals = []
    else:
        vals = vals.split(",")
        vals = [v.strip() for v in vals]
        vals = [re.sub("^\s*\d ", "", v) for v in  vals]
        vals = [re.sub(" bags?\.*", "", v) for v in vals]
    return (key, vals)

def build_graph_from(lines: List[str]) -> Dict[str, List[str]]:
    graph = {}
    for line in lines:
        key, vals = parse_line(line)
        graph[key] = vals
    return graph

def reachable(init: str, query: str, graph: Dict[str, List[str]]) -> bool:
    if 0 == len(graph[init]):
        return False
    if query in graph[init]:
        return True
    return any([reachable(n, query, graph) for n in graph[init]])

def main():
    graph = build_graph_from([line for line in lines()])
    count = sum([reachable(s, "shiny gold", graph) for s in graph.keys()])
    print(f"{count} bags can contain at least 1 shiny gold bag")

if __name__ == "__main__":
    main()