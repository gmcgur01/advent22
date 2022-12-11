#! /usr/bin/env python3

import sys
from dataclasses import dataclass

@dataclass
class Interval:
    start: int
    end: int

@dataclass
class Pair:
    elf1: Interval
    elf2: Interval
    
    def is_overlap(self):
        if self.elf1.start <= self.elf2.start and self.elf1.end >= self.elf2.end:
            return True
        if self.elf2.start <= self.elf1.start and self.elf2.end >= self.elf1.end:
            return True
        return False

def main():
    
    if len(sys.argv) != 2: 
        sys.exit(f"Usage: {sys.argv[0]} <file name>")

    pairs = []

    try:
        with open(sys.argv[1]) as file:
            for line in file:
                elf1, elf2 = line.strip().split(",")
                start, end = elf1.split("-")
                elf1 = Interval(int(start), int(end))
                start, end = elf2.split("-")
                elf2 = Interval(int(start), int(end))
                pairs.append(Pair(elf1, elf2))
    except FileNotFoundError:
        sys.exit(f"{sys.argv[1]}: Unable to open file")

    overlap_total = 0
    for pair in pairs:
        overlap_total += pair.is_overlap()

    print(overlap_total)

if __name__ == "__main__":
    main()