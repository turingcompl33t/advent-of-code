# kyle_part2.py
#
# Advent of Code Day 7 Puzzle 2.

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
        cnts = [int(v[0]) for v in vals]
        vals = [re.sub("^\s*\d ", "", v) for v in  vals]
        vals = [re.sub(" bags?\.*", "", v) for v in vals]
        for idx, cnt in enumerate(cnts):
            vals.extend([vals[idx] for _ in range(cnt - 1)])
    return (key, vals)

def build_graph_from(lines: List[str]) -> Dict[str, List[str]]:
    graph = {}
    for line in lines:
        key, vals = parse_line(line)
        graph[key] = vals
    return graph

def bags_contained_in(query: str, graph: Dict[str, List[str]]) -> bool:
    if 0 == len(graph[query]):
        return 0
    return len(graph[query]) + sum([bags_contained_in(q, graph) for q in graph[query]])

def main():
    graph = build_graph_from([line for line in lines()])
    total = bags_contained_in("shiny gold", graph)
    print(f"shiny gold bag contains {total} bags")

if __name__ == "__main__":
    main()