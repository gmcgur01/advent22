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

    max_elf = max(elves, key=get_total)

    print (get_total(max_elf))


if __name__ == "__main__":
    main()