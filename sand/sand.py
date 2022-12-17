#! /usr/bin/env python3
import sys
from dataclasses import dataclass

def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <file name>")

    rock_paths = []

    try:
        with open(sys.argv[1]) as file:
            for line in file:
                line = line.strip()
                rock_paths.append(parse_line(line))
    except FileNotFoundError:
        sys.exit(f"{sys.argv[1]}: Unable to open file")

    max_y = max(rock_paths[0], key=get_y).y

    for path in rock_paths:
        y = max(path, key=get_y).y
        if y > max_y: max_y = y

    cave_width = (2 * (max_y + 2)) + 1

    min_x = 500 - (max_y + 3)

    cave = [[0 for _ in range(cave_width + 1)] for _ in range(max_y + 3)]

    rock_paths.append([Position(min_x, max_y + 2), Position(min_x + cave_width, max_y + 2)])

    draw_paths(cave, rock_paths, min_x)

    print(drop_sand(cave, min_x))

@dataclass
class Position:
    x: int
    y: int

    def is_inbounds(self, grid):
        if self.y == len(grid) - 1: return False
        return True

def parse_line(line):
    path = []
    line_comps = line.split(" -> ")
    for comp in line_comps:
        x, y = comp.split(",")
        path.append(Position(int(x), int(y)))
    return path

def get_x(pos):
    return pos.x

def get_y(pos):
    return pos.y

def draw_paths(cave, paths, min_x):
    for path in paths:
        i = 0
        while i < (len(path) - 1):
            source = path[i]
            dest = path[i + 1]

            if source.x == dest.x:
                if source.y <= dest.y:
                    for j in range(source.y, dest.y + 1):
                        cave[j][source.x - min_x] = 1
                else:
                    for j in range(dest.y, source.y + 1):
                        cave[j][source.x - min_x] = 1
            elif source.y == dest.y:
                if source.x <= dest.x:
                    for j in range(source.x, dest.x + 1):
                        cave[source.y][j - min_x] = 1
                else:
                    for j in range(dest.x, source.x + 1):
                        cave[source.y][j - min_x] = 1
            else:
                raise ValueError("Path component is not a straight line")
            
            i += 1

def print_cave(cave):
    for row in cave:
        for spot in row:
            print (spot, end=" ")
        print("")

def drop_sand(cave, min_x):
    units = 0
    in_bounds = True
    can_move = False
    while in_bounds: 
        if not can_move:
            if cave[0][500 - min_x] == 1:
                return units
            sand = Position(500 - min_x, 0)
            can_move = True
            units += 1
        while can_move:
            if not sand.is_inbounds(cave): 
                in_bounds = False
                break
            if cave[sand.y + 1][sand.x] != 1:
                sand.y += 1
                continue
            if cave[sand.y + 1][sand.x - 1] != 1:
                sand.y += 1
                sand.x -= 1
                continue
            if cave[sand.y + 1][sand.x + 1] != 1:
                sand.y += 1
                sand.x += 1
                continue
            cave[sand.y][sand.x] = 1
            can_move = False
    return units

if __name__ == "__main__":
    main()