#! /usr/bin/env python3
import sys
from dataclasses import dataclass
import re
from functools import cache

def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <file name>")

    try:
        with open(sys.argv[1]) as file:
            blueprints = [parse_line(line.rstrip()) for line in file]
    except FileNotFoundError:
        sys.exit(f"{sys.argv[1]}: Unable to open file")

    quality_total = 0
    for i, blueprint in enumerate(blueprints):
        quality_total += (i + 1) * max_geodes(blueprint)

    print(quality_total)
        

def parse_line(line):
    if matches := re.findall(r"(-?\d+)", line):
        return Blueprint(*list(map(int, matches))[1:])
    raise ValueError("Invalid line")

@dataclass(frozen=True)
class Blueprint:
    ore_cost: int
    clay_cost: int
    obsidian_ore_cost: int
    obsidian_clay_cost: int
    geode_ore_cost: int
    geode_obsidian_cost: int

def max_geodes(blueprint):
    result = mine(24, blueprint, (0, 0, 0, 0), (1, 0, 0, 0), 0)
    print(result)
    return result 

# for mats and robots:
    # index 0 is ore
    # index 1 is clay
    # index 2 is obsidian 
    # index 3 is geodes
@cache
def mine(round_num, blueprint, mats, robots, curr_max):
    if curr_max > mats[3] + (robots[3] * round_num) + (((round_num) * (round_num - 1)) // 2):
        return 0
    
    if round_num > 2:
        new_mats = [mats[i] + robots[i] for i in range(4)]
        if mats[0] >= blueprint.geode_ore_cost and mats[2] >= blueprint.geode_obsidian_cost:
            spend_mats = (new_mats[0] - blueprint.geode_ore_cost, new_mats[1], new_mats[2] - blueprint.geode_obsidian_cost, new_mats[3])
            new_robots = (robots[0], robots[1], robots[2], robots[3] + 1)
            result = mine(round_num - 1, blueprint, spend_mats, new_robots, curr_max)
            if result > curr_max: 
                curr_max = result
        if mats[0] >= blueprint.obsidian_ore_cost and mats[1] >= blueprint.obsidian_clay_cost:
            spend_mats = (new_mats[0] - blueprint.obsidian_ore_cost, new_mats[1] - blueprint.obsidian_clay_cost, new_mats[2], new_mats[3])
            new_robots = (robots[0], robots[1], robots[2] + 1, robots[3])
            result = mine(round_num - 1, blueprint, spend_mats, new_robots, curr_max)
            if result > curr_max: 
                curr_max = result
        if mats[0] >= blueprint.clay_cost:
            spend_mats = (new_mats[0]  - blueprint.clay_cost, new_mats[1], new_mats[2], new_mats[3])
            new_robots = (robots[0], robots[1] + 1, robots[2], robots[3])
            result = mine(round_num - 1, blueprint, spend_mats, new_robots, curr_max)
            if result > curr_max: 
                curr_max = result
        if mats[0] >= blueprint.ore_cost:
            spend_mats = (new_mats[0]  - blueprint.ore_cost, new_mats[1], new_mats[2], new_mats[3])
            new_robots = (robots[0] + 1, robots[1], robots[2], robots[3])
            result = mine(round_num - 1, blueprint, spend_mats, new_robots, curr_max)
            if result > curr_max: 
                curr_max = result
        
        result = mine(round_num - 1, blueprint, tuple(new_mats), robots, curr_max)
        if result > curr_max: 
            curr_max = result
        
        return curr_max

    # second to last round, only buy geode robots:
    if round_num == 2:

        new_mats = [mats[i] + robots[i] for i in range(4)]
        
        if mats[0] >= blueprint.geode_ore_cost and mats[2] >= blueprint.geode_obsidian_cost:
            spend_mats = (new_mats[0] - blueprint.geode_ore_cost, new_mats[1], new_mats[2] - blueprint.geode_obsidian_cost, new_mats[3])
            new_robots = (robots[0], robots[1], robots[2], robots[3] + 1)
            result = mine(round_num - 1, blueprint, spend_mats, new_robots, curr_max)
            if result > curr_max: 
                curr_max = result

        result = mine(round_num - 1, blueprint, tuple(new_mats), robots, curr_max)
        if result > curr_max: 
            curr_max = result

        return curr_max

    # last round, don't buy robots
    if round_num == 1:
        new_mats = [mats[i] + robots[i] for i in range(4)]

        result = mine(round_num - 1, blueprint, tuple(new_mats), robots, curr_max)
        if result > curr_max: 
            curr_max = result

        return curr_max

    if round_num == 0:
        return mats[3]
    

if __name__ == "__main__":
    main()