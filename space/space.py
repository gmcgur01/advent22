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

    root = Directory(0, [], {}, None)

    for line in terminal_output:
        components = line.split(" ")
        if components[0] == "$":
            if components[1] == "cd":
                if components[2] == "..":
                    curr_dir = curr_dir.parent
                elif components[2] == "/":
                    curr_dir = root
                else:
                    curr_dir = curr_dir.subdirectories[components[2]]
        else:
            if components[0] == "dir":
                curr_dir.subdirectories[components[1]] = Directory(0, [], {}, curr_dir)
            else:
                curr_dir.files.append(int(components[0]))

    print(root)
    calculate_size(root)

@dataclass
class Directory:
    total_size: int
    files: list
    subdirectories: dict
    parent: any

def calculate_size(dir):
    dir.size = sum(dir.files)
    for subdir in dir.subdirectories:
        dir.size += calculate_size(subdir)
        

if __name__ == "__main__":
    main()