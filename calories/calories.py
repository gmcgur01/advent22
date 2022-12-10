#! python3

import sys
from dataclasses import dataclass


class Elf:
    
    def __init__(self):
        self.calories = []

    def __str__(self):
        ret = "Elf:"
        for calorie in self.calories:
            ret = ret + str(calorie) + " "
        return ret

    def __eq__(self, other):
        return self.calories == other.calories

    def __ne__(self, other):
        return not self == other
    
def get_total(elf):
        return sum(elf.calories)

def main():

    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <file name>")

    try:
        with open(sys.argv[1]) as fp:
            file = fp.readlines()

    except FileNotFoundError:
        sys.exit(f"{sys.argv[1]}: Unable to open the file")

    elves = []

    curr_elf = Elf()
    for line in file:
        if line == "\n":
            elves.append(curr_elf)
            curr_elf = Elf()
        else:
            curr_elf.calories.append(int(line.strip()))

    elves.append(curr_elf)

    max_elves = []

    for _ in range(3):
        max_elf = max(elves, key=get_total)
        max_elves.append(max_elf)
        elves.remove(max_elf)

    total = 0
    for elf in max_elves:
        total += get_total(elf)

    print(total)

if __name__ == "__main__":
    main()