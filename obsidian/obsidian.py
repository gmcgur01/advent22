#! /usr/bin/env python3
import sys
import re
from dataclasses import dataclass

def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <file name>")
    try:
        with open(sys.argv[1]) as file:
            coords = [parse_line(line) for line in file]
    except FileNotFoundError:
        sys.exit(f"{sys.argv[1]}: Unable to open file")

    surface_area = len(coords) * 6

    for i, coord1 in enumerate(coords):
        for coord2 in coords[i+1:]:
            if coord1.is_adj(coord2):
                surface_area -= 2

    print(surface_area)

def parse_line(line):
    if matches := re.findall(r"\d+", line):
        matches = [int(match) for match in matches]
        return Coord(*matches)
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
if __name__ == "__main__":
    main()