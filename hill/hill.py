#! /usr/bin/env python3
import sys

from dataclasses import dataclass
from collections import deque

def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <file name>")

    grid = []

    try:
        with open(sys.argv[1]) as file:
            for line in file:
                line = line.strip()
                row = []
                for i in range(len(line)):
                    new_pos = Position(line[i], len(grid), i, False)
                    if new_pos.value == "S":
                        start = new_pos
                    row.append(new_pos)
                grid.append(row)
    except FileNotFoundError:
        sys.exit(f"{sys.argv[1]}: Unable to open file")

    queue = deque()

    queue.append(BFS_Node(start, 0))

    while len(queue) != 0:
        curr_node = queue[0]
        if curr_node.pos.value == "E":
            print (curr_node.path_length)
            break
        # check up
        if can_visit(grid, curr_node.pos, curr_node.pos.row_num - 1, curr_node.pos.col_num):
            grid[curr_node.pos.row_num - 1][curr_node.pos.col_num].visited = True
            queue.append(BFS_Node(grid[curr_node.pos.row_num - 1][curr_node.pos.col_num], curr_node.path_length + 1))
        # check down
        if can_visit(grid, curr_node.pos, curr_node.pos.row_num + 1, curr_node.pos.col_num):
            grid[curr_node.pos.row_num + 1][curr_node.pos.col_num].visited = True
            queue.append(BFS_Node(grid[curr_node.pos.row_num + 1][curr_node.pos.col_num], curr_node.path_length + 1))
        # check left
        if can_visit(grid, curr_node.pos, curr_node.pos.row_num, curr_node.pos.col_num - 1):
            grid[curr_node.pos.row_num][curr_node.pos.col_num - 1].visited = True
            queue.append(BFS_Node(grid[curr_node.pos.row_num][curr_node.pos.col_num - 1], curr_node.path_length + 1))
        # check right
        if can_visit(grid, curr_node.pos, curr_node.pos.row_num, curr_node.pos.col_num + 1):
            grid[curr_node.pos.row_num][curr_node.pos.col_num + 1].visited = True
            queue.append(BFS_Node(grid[curr_node.pos.row_num][curr_node.pos.col_num + 1], curr_node.path_length + 1))
        queue.popleft()

@dataclass
class Position:
    value: str
    row_num: int 
    col_num: int
    visited: bool

    def get_height(self):
        if self.value == "S":
            return -1
        if self.value == "E":
            return 26
        return ord(self.value) - 97

@dataclass
class BFS_Node:
    pos: Position
    path_length: int

def can_visit(grid, curr_pos, row_num, col_num):
    if row_num < 0 or row_num >= len(grid) or col_num < 0 or col_num >= len(grid[0]):
        return False
    if grid[row_num][col_num].visited:
        return False
    if grid[row_num][col_num].get_height() - curr_pos.get_height() <= 1:
        return True

if __name__ == "__main__":
    main()