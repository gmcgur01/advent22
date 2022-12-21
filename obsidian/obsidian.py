#! /usr/bin/env python3
import sys
import re
from dataclasses import dataclass

def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <file name>")
    try:
        with open(sys.argv[1]) as file:
            coords = [parse_line(line.strip()) for line in file]
    except FileNotFoundError:
        sys.exit(f"{sys.argv[1]}: Unable to open file")

    fill_center(coords)

    print(surface_area(coords))

def surface_area(coords):
    
    surface_area = len(coords) * 6

    for i, coord1 in enumerate(coords):
        for coord2 in coords[i+1:]:
            if coord1.is_adj(coord2) and coord1 != coord2:
                surface_area -= 2

    return surface_area

def parse_line(line):
    if matches := re.findall(r"\d+", line):
        return Coord(*[int(match) for match in matches])
    raise ValueError("Improperly formatted line")

@dataclass
class Coord:
    x: int
    y: int
    z: int

    def is_adj(self, other):
        if self.x == other.x and self.y == other.y:
            return abs(self.z - other.z) <= 1
        if self.x == other.x and self.z == other.z:
            return abs(self.y - other.y) <= 1
        if self.y == other.y and self.z == other.z:
            return abs(self.x - other.x) <= 1
        return False

def fill_center(coords):

    min_x = min(coords, key=lambda c: c.x).x - 1
    max_x = max(coords, key=lambda c: c.x).x + 1
    x_len = max_x - min_x

    min_y = min(coords, key=lambda c: c.y).y - 1
    max_y = max(coords, key=lambda c: c.y).y + 1
    y_len = max_y - min_y

    min_z = min(coords, key=lambda c: c.z).z - 1
    max_z = max(coords, key=lambda c: c.z).z + 1
    z_len = max_z - min_z

    volume = [[[Coord(x,y,z) in coords for x in range(min_x, max_x + 1)] for y in range(min_y, max_y + 1)] for z in range(min_z, max_z + 1)]

    # dfs to find air pockets
    exterior = []

    exterior.append(Coord(min_x, min_y, min_z))
    volume[min_z][min_y][min_x] = True

    while len(exterior) != 0:
        curr_coord = exterior.pop()
        if curr_coord.x != min_x and not volume[curr_coord.z - min_z][curr_coord.y - min_y][curr_coord.x - 1 - min_x]:
            volume[curr_coord.z - min_z][curr_coord.y - min_y][curr_coord.x - 1 - min_x] = True
            exterior.append(Coord(curr_coord.x - 1, curr_coord.y, curr_coord.z))

        if curr_coord.x != max_x and not volume[curr_coord.z - min_z][curr_coord.y - min_y][curr_coord.x + 1 - min_x]:
            volume[curr_coord.z - min_z][curr_coord.y - min_y][curr_coord.x + 1 - min_x] = True
            exterior.append(Coord(curr_coord.x + 1, curr_coord.y, curr_coord.z))

        if curr_coord.y != min_y and not volume[curr_coord.z - min_z][curr_coord.y - 1 - min_y][curr_coord.x - min_x]:
            volume[curr_coord.z - min_z][curr_coord.y - 1 - min_y][curr_coord.x - min_x] = True
            exterior.append(Coord(curr_coord.x, curr_coord.y - 1, curr_coord.z))

        if curr_coord.y != max_y and not volume[curr_coord.z - min_z][curr_coord.y + 1 - min_y][curr_coord.x - min_x]:
            volume[curr_coord.z - min_z][curr_coord.y + 1 - min_y][curr_coord.x - min_x] = True
            exterior.append(Coord(curr_coord.x, curr_coord.y + 1, curr_coord.z))

        if curr_coord.z != min_z and not volume[curr_coord.z - 1 - min_z][curr_coord.y - min_y][curr_coord.x - min_x]:
            volume[curr_coord.z - 1 - min_z][curr_coord.y - min_y][curr_coord.x - min_x] = True
            exterior.append(Coord(curr_coord.x, curr_coord.y, curr_coord.z - 1))

        if curr_coord.z != max_z and not volume[curr_coord.z + 1 - min_z][curr_coord.y - min_y][curr_coord.x - min_x]:
            volume[curr_coord.z + 1 - min_z][curr_coord.y - min_y][curr_coord.x - min_x] = True
            exterior.append(Coord(curr_coord.x, curr_coord.y, curr_coord.z + 1))

    for z in range(z_len):
        for y in range(y_len):
            for x in range(x_len):
                if not volume[z - min_z][y - min_y][x - min_x]:
                    coords.append(Coord(x, y, z))

if __name__ == "__main__":
    main()