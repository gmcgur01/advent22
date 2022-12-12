#! /usr/bin/env python3
import sys
from dataclasses import dataclass

def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <file name>")

    grid = []

    try:
        with open(sys.argv[1]) as file:
            for line in file:
                trees = line.strip()
                row = []
                for tree_num in range(len(trees)):
                    row.append(Tree(int(trees[tree_num]), len(grid), tree_num))
                grid.append(row)
    except FileNotFoundError:
        sys.exit(f"{sys.argv[1]}: Unable to open file")

    grid_height = len(grid)
    grid_width = len(grid[0])

    max_score = -1

    for row_num in range(grid_height):
        for col_num in range(grid_width):
            scenic_score = 1
            scenic_score *= scenic_left(grid, grid[row_num][col_num].height, row_num, col_num)
            scenic_score *= scenic_right(grid, grid[row_num][col_num].height, row_num, col_num)
            scenic_score *= scenic_up(grid, grid[row_num][col_num].height, row_num, col_num)
            scenic_score *= scenic_down(grid, grid[row_num][col_num].height, row_num, col_num)
            if scenic_score > max_score:
                max_score = scenic_score
    
    print (max_score)


@dataclass(frozen=True)
class Tree:
    height: int
    row_num: int
    col_num: int

    def __str__(self):
        return str(self.height)

def get_visible(grid):

    grid_height = len(grid)
    grid_width = len(grid[0])

    visible_trees = set()

    for row_num in range(grid_height):
        left_tallest = -1
        right_tallest = -1
        for col_num in range(grid_width):
            if grid[row_num][col_num].height > left_tallest:
                left_tallest = grid[row_num][col_num].height
                if grid[row_num][col_num] not in visible_trees:
                    visible_trees.add(grid[row_num][col_num])
            if grid[row_num][grid_width - col_num - 1].height > right_tallest:
                right_tallest = grid[row_num][grid_width - col_num - 1].height
                if grid[row_num][grid_width - col_num - 1] not in visible_trees:
                    visible_trees.add(grid[row_num][grid_width - col_num - 1])


    for col_num in range(grid_width):
        above_tallest = -1
        below_tallest = -1
        for row_num in range(grid_height):
            if grid[row_num][col_num].height > above_tallest:
                above_tallest = grid[row_num][col_num].height
                if grid[row_num][col_num] not in visible_trees:
                    visible_trees.add(grid[row_num][col_num])
            if grid[grid_height - row_num - 1][col_num].height > below_tallest:
                below_tallest = grid[grid_height - row_num - 1][col_num].height
                if grid[grid_height - row_num - 1][col_num] not in visible_trees:
                    visible_trees.add(grid[grid_height - row_num - 1][col_num])

    return len(visible_trees)

def scenic_left(grid, height, row_num, col_num):
    scenic_score = 0
    if col_num == 0:
        return scenic_score
    col_num -= 1
    curr_tree = grid[row_num][col_num]
    scenic_score += 1
    while curr_tree.height < height:
        col_num -= 1
        if col_num < 0:
            break
        curr_tree = grid[row_num][col_num]
        scenic_score += 1
    return scenic_score

def scenic_right(grid, height, row_num, col_num):
    scenic_score = 0
    if col_num == len(grid[0]) - 1:
        return scenic_score
    col_num += 1
    curr_tree = grid[row_num][col_num]
    scenic_score += 1
    while curr_tree.height < height:
        col_num += 1
        if col_num >= len(grid[0]):
            break
        curr_tree = grid[row_num][col_num]
        scenic_score += 1
    return scenic_score

def scenic_up(grid, height, row_num, col_num):
    scenic_score = 0
    if row_num == 0:
        return scenic_score
    row_num -= 1
    curr_tree = grid[row_num][col_num]
    scenic_score += 1
    while curr_tree.height < height:
        row_num -= 1
        if row_num < 0:
            break
        curr_tree = grid[row_num][col_num]
        scenic_score += 1
    return scenic_score

def scenic_down(grid, height, row_num, col_num):
    scenic_score = 0
    if row_num == len(grid) - 1:
        return scenic_score
    row_num += 1
    curr_tree = grid[row_num][col_num]
    scenic_score += 1
    while curr_tree.height < height:
        row_num += 1
        if row_num >= len(grid):
            break
        curr_tree = grid[row_num][col_num]
        scenic_score += 1
    return scenic_score

if __name__ == "__main__":
    main()