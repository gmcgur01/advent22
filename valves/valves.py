#! /usr/bin/env python3
import sys
import re
from dataclasses import dataclass
from collections import deque
from functools import cache

valves = []
working_valves = []
grid = []

def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <file name>")

    try:
        with open(sys.argv[1]) as file:
            for line in file:
                valves.append(parse_line(line.strip()))
    except FileNotFoundError:
        sys.exit(f"{sys.argv[1]}: Unable to open file")
    
    link_valves(valves)

    shortest_path(valves)
    
    start = 0

    for valve in valves:
        if valve.name == "AA":
            start = valves.index(valve)
        if valve.flow != 0:
            working_valves.append(valve)

    print(split_list(start))

def parse_line(line):
    if matches := re.findall(r"([A-Z][A-Z]|(?:\d+))", line):
        return Valve(matches[0], int(matches[1]), matches[2:])

def link_valves(valves):
    for valve in valves:
        for neighbor in valve.neighbors:
            for inner_valve in valves:
                if neighbor == inner_valve.name:
                    valve.neighbors[valve.neighbors.index(neighbor)] = inner_valve
                    break

def shortest_path(valves):

    for _ in range(len(valves)):
        grid.append([0 for _ in range(len(valves))])
    
    for valve in valves:
        queue = deque()
        seen = set()
        queue.append((valve, 0))
        seen.add(valve.name)
        while len(queue) != 0:
            curr_valve, steps = queue[0]
            queue.popleft()
            grid[valves.index(valve)][valves.index(curr_valve)] = steps
            for neighbor in curr_valve.neighbors:
                if neighbor.name not in seen:
                    queue.append((neighbor, steps + 1))
                    seen.add(neighbor.name)
        
@cache
def max_flow(curr_index, time, visited, working):
    if time <= 0:
        return 0
    max = 0
    for i in range(len(working)):
        if (1 << i) & visited == 0:
            next_index = working[i]
            new_time = time - (grid[curr_index][next_index] + 1)
            new_visited = visited | (1 << i)
            ret = max_flow(next_index, new_time, new_visited, working)
            if ret > max: max = ret
    return (valves[curr_index].flow * time) + max

def split_list(start):
    max = 0
    for i in range(1 << len(working_valves)):
        group1 = []
        group2 = []
        for j in range(len(working_valves)):
            if (1 << j) & i == 0:
                group1.append(valves.index(working_valves[j]))
            else:
                group2.append(valves.index(working_valves[j]))
        val = max_flow(start, 26, 0, tuple(group1)) + max_flow(start, 26, 0, tuple(group2))
        if val > max:
            max = val
    return max

@dataclass
class Valve:
    name: str
    flow: int
    neighbors: list

    def __repr__(self):
        return self.name

    def __str__(self):
        ret = f"Name: {self.name}, Flow: {self.flow}, Neighbors: "
        for neighbor in self.neighbors:
            ret += neighbor.name + " "
        return ret
        
if __name__ == "__main__":
    main()