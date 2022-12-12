#! /usr/bin/env python3

import sys
from dataclasses import dataclass

def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <file name>")

    terminal_output = []

    try:
        with open(sys.argv[1]) as file:
            for line in file:
                terminal_output.append(line.strip())
    except FileNotFoundError:
        sys.exit(f"{sys.argv[1]}: Unable to open file")

    root = Directory("/", 0, [], {}, None)

    for line in terminal_output:
        comp = line.split(" ")
        if comp[0] == "$":
            if comp[1] == "cd":
                if comp[2] == "..":
                    curr_dir = curr_dir.parent
                elif comp[2] == "/":
                    curr_dir = root
                else:
                    curr_dir = curr_dir.subdirectories[comp[2]]
        else:
            if comp[0] == "dir":
                curr_dir.subdirectories[comp[1]] = Directory(comp[1], 0, [], {}, curr_dir)
            else:
                curr_dir.files.append(int(comp[0]))

    calculate_size(root)

    unused_space = 70000000 - root.size
    space_to_free = 30000000 - unused_space

    print (find_smallest(root, space_to_free).size)


@dataclass
class Directory:
    name: str
    total_size: int
    files: list[int]
    subdirectories: dict
    parent: any

def calculate_size(dir):
    dir.size = sum(dir.files)
    for subdir in dir.subdirectories.values():
        calculate_size(subdir)
        dir.size += subdir.size

def calculate_sum(dir):
    sum = 0
    if dir.size <= 100000:
        sum += dir.size
    for subdir in dir.subdirectories.values():
        sum += calculate_sum(subdir)
    return sum
        
def find_smallest(dir, size):
    ret = None
    if dir.size > size:
        ret = dir
    for subdir in dir.subdirectories.values():
        result = find_smallest(subdir, size)
        if result != None and result.size < ret.size:
            ret = result
    return ret

if __name__ == "__main__":
    main()