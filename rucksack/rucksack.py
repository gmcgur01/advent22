#! /usr/bin/env python3

import sys

class Group:
    def __init__(self, sacks):
        self.sacks = sacks

    def find_badge(self):
        for item in self.sacks[0]: 
            if item in self.sacks[1] and item in self.sacks[2]: 
                return item
        raise Exception("No common item found")

def main():

    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <file name>")

    rucksacks = []

    try:
        with open(sys.argv[1]) as file:
            for line in file:
                rucksacks.append(line.strip())
    except FileNotFoundError:
        sys.exit(f"{sys.argv[1]}: Unable to open file")


    groups = []

    for i in range(len(rucksacks)):
        if i % 3 == 0: 
            curr_group = Group([])
            groups.append(curr_group)
        curr_group.sacks.append(rucksacks[i])

    priority_total = 0

    for group in groups:
        priority_total += get_priority(group.find_badge())

    print(priority_total)


def get_priority(item):
    if item.islower(): return ord(item) - 96
    if item.isupper(): return ord(item) - 38
    raise ValueError("invalid item")

if __name__ == "__main__":
    main()