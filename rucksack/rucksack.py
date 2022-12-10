#! /usr/bin/env python3

import sys

def main():

    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <file name>")

    priority_total = 0

    try:
        with open(sys.argv[1]) as file:
            for line in file:
                priority_total += get_priority(find_dupe(line))
    except FileNotFoundError:
        sys.exit(f"{sys.argv[1]}: Unable to open file")

    print (priority_total)

def get_priority(item):
    if item.islower(): return ord(item) - 96
    if item.isupper(): return ord(item) - 38
    raise ValueError("invalid item")

def find_dupe(rucksack):
    for item in rucksack[0:int(len(rucksack)/2)]:
        if item in rucksack[int(len(rucksack)/2):]:
            return item
    raise Exception("No duplicate found")

if __name__ == "__main__":
    main()