#! /usr/bin/env python3
import sys
from dataclasses import dataclass
import math

def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <file name>")
    try:
        with open(sys.argv[1]) as file:
            jet_pattern = file.readline().strip()
    except FileNotFoundError:
        sys.exit(f"{sys.argv[1]}: Unable to open file")

    start, end = find_cycle(Cave(jet_pattern))
    # how many rocks in each cycle
    cycle_length = end[0] - start[0]
    # get the offset height (height until the start of cycle + extra at the end)
    offset = get_height(Cave(jet_pattern), ((1000000000000 - start[0]) % cycle_length) + start[0])
    # calculate the number of cycles needed to reach 1 trillion
    num_cycles = math.floor((1000000000000 - start[0]) / cycle_length)
    
    print(num_cycles * (end[1] - start[1]) + offset)

class Cave:
    def __init__(self, jet_pattern):
        self.cave = []
        self.jet_pattern = jet_pattern
        self.jet_len = len(jet_pattern)

    def get_jet(self, round_num):
        return self.jet_pattern[round_num % self.jet_len]

    def generate_rock(self, round_num):
        empty_rows = len(self.cave) - self.cave_height()
        if empty_rows < 3:
            for _ in range(3 - empty_rows):
                self.add_row([0 for _ in range(7)])
        elif empty_rows > 3:
            for _ in range(empty_rows - 3):
                self.rem_row()
        match round_num % 5:
            case 0:
                self.add_row([0 for _ in range(7)])
                return Rock(self, 0)
            case 1:
                for _ in range(3): self.add_row([0 for _ in range(7)]) 
                return Rock(self, 1)
            case 2:
                for _ in range(3): self.add_row([0 for _ in range(7)]) 
                return Rock(self, 2)
            case 3:
                for _ in range(4): self.add_row([0 for _ in range(7)]) 
                return Rock(self, 3)
            case 4:
                for _ in range(2): self.add_row([0 for _ in range(7)]) 
                return Rock(self, 4)

    def print_cave(self):
        for row in reversed(self.cave):
            print(row)

    def cave_height(self):
        i = len(self.cave)
        while i > 0:
            if not self.cave[i - 1] == [0 for _ in range(7)]:
                return i
            i -= 1
        return 0

    def col_height(self, col_num):
        tallest = self.cave_height()
        i = tallest - 1
        while i != -1 and (self.cave[i][col_num]) != 1:
            i -= 1
        return tallest - (i + 1)
        
    def add_row(self, row):
        if len(row) != 7:
            raise ValueError("Cave row must be 7 elements long")
        self.cave.append(row)

    def rem_row(self):
        if len(self.cave) == 0:
            raise ValueError("Can't remove a row from an empty cave")
        self.cave.pop()

class Rock:
    def __init__(self, cave, rock_type):
        self.cave = cave
        top = len(self.cave.cave) - 1
        match rock_type:
            case 0:
                self.points = [Point(i, top) for i in range(2,6)]
            case 1:
                self.points = [Point(3, top), Point(2, top - 1), Point(3, top - 1), Point(4, top - 1), Point(3, top - 2)]
            case 2:
                self.points = [Point(4, top), Point(4, top - 1), Point(2, top - 2), Point(3, top - 2), Point(4, top - 2)]
            case 3: 
                self.points = [Point(2, top - i) for i in range(4)]
            case 4:
                self.points = [Point(2, top), Point(3, top), Point(2, top - 1), Point(3, top - 1)]
            case _:
                raise ValueError("Invalid rock type")

    def draw_rock(self):
        for point in self.points:
            self.cave.cave[point.y][point.x] = 1

    def move_down(self):
        for point in self.points:
            if point.y == 0:
                return False
            if self.cave.cave[point.y - 1][point.x] == 1:
                return False
        for point in self.points:
            point.y -= 1
        return True

    def move_left(self):
        for point in self.points:
            if point.x == 0:
                return False
            if self.cave.cave[point.y][point.x - 1] == 1:
                return False
        for point in self.points:
            point.x -= 1
        return True
    
    def move_right(self):
        for point in self.points:
            if point.x == 6:
                return False
            if self.cave.cave[point.y][point.x + 1] == 1:
                return False
        for point in self.points:
            point.x += 1
        return True

@dataclass
class Point:
    x: int
    y: int

def find_cycle(cave):
    # dict used to store states; if the same state occurs twice, we have a cycle
    states = {}
    rock_total = 0
    round_num = 0
    new_rock = True
    while True:
        if new_rock:
            curr_rock = cave.generate_rock(rock_total)
            new_rock = False
        if cave.get_jet(round_num) == "<":
            curr_rock.move_left()
        else:
            curr_rock.move_right()
        if not curr_rock.move_down():
            curr_rock.draw_rock()
            new_rock = True
            # state is the round_num (how far into the jet pattern we are), 
            # the rock type, and the height difference for all 7 columns
            curr_state = tuple([round_num, rock_total % 5, tuple([cave.col_height(i) for i in range(7)])])
            if curr_state in states:
                return states[curr_state], (rock_total, cave.cave_height())
            else:
                states[curr_state] = (rock_total, cave.cave_height())
            rock_total += 1
        round_num = ((round_num +  1) % cave.jet_len)

def get_height(cave, rocks):
    rock_total = 0
    round_num = 0
    new_rock = True
    while rock_total < rocks:
        if new_rock:
            curr_rock = cave.generate_rock(rock_total)
            new_rock = False
        if cave.get_jet(round_num) == "<":
            curr_rock.move_left()
        else:
            curr_rock.move_right()
        if not curr_rock.move_down():
            curr_rock.draw_rock()
            new_rock = True
            rock_total += 1
        round_num = ((round_num +  1) % cave.jet_len)

    return cave.cave_height()

if __name__ == "__main__":
    main()