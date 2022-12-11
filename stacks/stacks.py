#! /usr/bin/env python3

import sys
from dataclasses import dataclass

class Instruction:
    num_boxes: int
    source: int
    destination: int

def main():
    
    if len(sys.argv) != 2: 
        sys.exit(f"Usage: {sys.argv[0]} <file name>")

    
    drawing = []
    instructions = []

    try:
        with open(sys.argv[1]) as file:
            receiver = drawing
            for line in file:
                if line.strip() == "":
                    receiver = instructions
                    continue
                receiver.append(line)

    except FileNotFoundError:
        sys.exit(f"{sys.argv[1]}: Unable to open file")


    last_line = drawing.pop()
    num_stacks = int(last_line[len(last_line) - 3])

    stacks = [[] for _ in range(num_stacks)]

    drawing.reverse()
    for line in drawing:
        for i in range(num_stacks):
            if line[(4 * i) + 1] != " ":
                stacks[i].append(line[(4 * i) + 1])

    move_stack = []

    for instruction in instructions:
        instr = instruction.strip().split(" ")
        for _ in range(int(instr[1])):
            box = stacks[int(instr[3]) - 1].pop()
            move_stack.append(box)
        while len(move_stack) != 0:
            box = move_stack.pop()
            stacks[int(instr[5]) - 1].append(box)

    for stack in stacks:
        print(stack.pop(), end="")
    print("")


if __name__ == "__main__":
    main()