#! /usr/bin/env python3
import sys
import re
from dataclasses import dataclass
from collections import deque
from itertools import permutations

def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <file name>")

    valves = []

    try:
        with open(sys.argv[1]) as file:
            for line in file:
                valves.append(parse_line(line.strip()))
    except FileNotFoundError:
        sys.exit(f"{sys.argv[1]}: Unable to open file")
    
    link_valves(valves)

    paths = shortest_path(valves)

    working_valves = []
    start = None

    for valve in valves:
        if valve.name == "AA":
            start = valve
        if valve.flow != 0:
            working_valves.append(valve)

    print(max_flow(valves, working_valves, paths, start))

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

    grid = [[0 for _ in range(len(valves))] for _ in range(len(valves))]
    
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
    
    return grid
        
def max_flow(valves, working_valves, grid, start):
    
    perms = permutations(working_valves)
    max_flow = 0
    count = 0
    for perm in perms:
        count += 1
        if not count % 1000000: print (count)
        curr_valve = start
        time = 30
        total = 0
        for valve in perm:
            time_spent = grid[valves.index(curr_valve)][valves.index(valve)] + 1
            time -= time_spent
            if time < 0:
                break
            total += valve.flow * time
            curr_valve = valve
        if total > max_flow:
            max_flow = total
    return max_flow

@dataclass
class Valve:
    name: str
    flow: int
    neighbors: list

    def __str__(self):
        ret = f"Name: {self.name}, Flow: {self.flow}, Neighbors: "
        for neighbor in self.neighbors:
            ret += neighbor.name + " "
        return ret
        
if __name__ == "__main__":
    main()