#! /usr/bin/env python3

import sys
from dataclasses import dataclass

@dataclass
class Turn:
    other_move: str
    my_move: str

def play_turn(other_move, my_move):

    points = 0
    match my_move:
        case "X":
            if other_move == "A": points += 3
            if other_move == "B": points += 1
            if other_move == "C": points += 2
        case "Y":
            points += 3
            if other_move == "A": points += 1
            if other_move == "B": points += 2
            if other_move == "C": points += 3
        case "Z":
            points += 6
            if other_move == "A": points += 2
            if other_move == "B": points += 3
            if other_move == "C": points += 1
        case _:
            raise ValueError("Invalid Move")

    return points

def main():

    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <file name>")

    game = []

    try: 
        with open(sys.argv[1]) as file:
            for line in file:
                other_move, my_move = line.strip().split(" ")
                game.append(Turn (other_move, my_move))
    except FileNotFoundError:
        sys.exit(f"{sys.argv[1]}: Unable to open file")

    total_points = 0
    for turn in game:
        total_points += play_turn(turn.other_move, turn.my_move)

    print(total_points)
        

if __name__ == "__main__":
    main()