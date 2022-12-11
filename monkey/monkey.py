#! /usr/bin/env python3

import sys
from dataclasses import dataclass
from collections import deque

@dataclass
class Monkey:
    items: deque
    op: any
    test: int
    true_case: int 
    false_case: int
    inspections: int

def get_inspections(monkey):
    return monkey.inspections

@dataclass
class Operation:
    left: int
    operand: str
    right: int

    def perform_op(self, old):
        if self.left == "old":
            left_op = old
        else:
            left_op = self.left

        if self.right == "old":
            right_op = old
        else:
            right_op = self.right

        match self.operand:
            case "+": return left_op + right_op
            case "*": return left_op * right_op
            case "-": return left_op - right_op
            case "/": return left_op / right_op
            case _: raise ValueError("Invalid operator")

def main():

    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <file name>")

    monkeys = []
    curr_monkey = None

    try:
        with open(sys.argv[1]) as file:
            for line in file:
                if line == "\n":
                    continue
                comps = line.strip().split(":")
                if "Monkey" in comps[0]:
                    curr_monkey = Monkey(deque(), None, -1, -1, -1, 0)
                    monkeys.append(curr_monkey)
                if comps[0] == "Starting items":
                    items = comps[1].strip().split(", ")
                    for item in items:
                        curr_monkey.items.append(int(item))
                if comps[0] == "Operation":
                    op_comps = comps[1].strip().split(" ")
                    left, right = "old", "old"
                    if op_comps[2] != "old":
                        left = int(op_comps[2])
                    if op_comps[4] != "old":
                        right = int(op_comps[4])
                    curr_monkey.op = Operation(left, op_comps[3], right)
                if comps[0] == "Test":
                    test = comps[1].strip().split(" ")
                    curr_monkey.test = int(test[2])
                if comps[0] == "If true":
                    curr_monkey.true_case = int(comps[1][len(comps[1]) - 1])
                if comps[0] == "If false":
                    curr_monkey.false_case = int(comps[1][len(comps[1]) - 1])

    except FileNotFoundError:
        sys.exit(f"{sys.argv[1]}: Unable to open file")

    for _ in range(20):

        for monkey in monkeys:
            while len(monkey.items) != 0:
                curr_item = monkey.items.popleft()
                curr_item = monkey.op.perform_op(curr_item)
                curr_item = int (curr_item / 3)
                if curr_item % monkey.test == 0:
                    monkeys[monkey.true_case].items.append(curr_item)
                else:
                    monkeys[monkey.false_case].items.append(curr_item)
                monkey.inspections += 1

    max_monkey = max(monkeys, key=get_inspections)
    monkey_business = get_inspections(max_monkey)
    monkeys.remove(max_monkey)

    max_monkey = max(monkeys, key=get_inspections)
    monkey_business *= get_inspections(max_monkey)

    print (monkey_business)






if __name__ == "__main__":
    main()