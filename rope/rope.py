import sys
from dataclasses import dataclass

@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

@dataclass(frozen=True)
class Move:
    direction: str
    num_steps: int


class Rope_segment:
    curr_poss: Coordinate
    visited_coords: set

    def __init__(self):
        self.curr_pos = Coordinate(0, 0)
        self.visited_coords = set()
        self.visited_coords.add(self.curr_pos)
        

    def in_range(self, other):
        if not isinstance(other, Rope_segment):
            raise ValueError("Parameter for in_range must be a rope end")
        if abs(self.curr_pos.x - other.curr_pos.x) > 1:
            return False
        if abs(self.curr_pos.y - other.curr_pos.y) > 1:
            return False
        return True

    def move(self, direction: str):
        match direction:
            case "U":
                new_pos = Coordinate(self.curr_pos.x, self.curr_pos.y + 1)
            case "D":
                new_pos = Coordinate(self.curr_pos.x, self.curr_pos.y - 1)
            case "L":
                new_pos = Coordinate(self.curr_pos.x - 1, self.curr_pos.y)
            case "R":
                new_pos = Coordinate(self.curr_pos.x + 1, self.curr_pos.y)
            case "UR":
                new_pos = Coordinate(self.curr_pos.x + 1, self.curr_pos.y + 1)
            case "DR":
                new_pos = Coordinate(self.curr_pos.x + 1, self.curr_pos.y - 1)
            case "UL":
                new_pos = Coordinate(self.curr_pos.x - 1, self.curr_pos.y + 1)
            case "DL":
                new_pos = Coordinate(self.curr_pos.x - 1, self.curr_pos.y - 1)
            case _:
                raise ValueError("Invalid direction")

        self.curr_pos = new_pos
        if self.curr_pos not in self.visited_coords:
            self.visited_coords.add(self.curr_pos)

    def follow(self, other):
        if not isinstance(other, Rope_segment):
            raise ValueError("Parameter for in_range must be a rope end")
        x_diff = other.curr_pos.x - self.curr_pos.x
        y_diff = other.curr_pos.y - self.curr_pos.y

        if x_diff < 0:
            if y_diff < 0: 
                self.move("DL")
            elif y_diff > 0:
                self.move("UL")
            else:
                self.move("L")
        elif x_diff > 0:
            if y_diff < 0: 
                self.move("DR")
            elif y_diff > 0:
                self.move("UR")
            else:
                self.move("R")
        else:
            if y_diff < 0: 
                self.move("D")
            elif y_diff > 0:
                self.move("U")
            else:
                raise ValueError("Can't follow")
        



def main():
    
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 rope.py <filename>")

    try:
        file = open(sys.argv[1])
    except FileNotFoundError:
        sys.exit(f"Unable to open: {sys.argv[1]}")

    moves = []
    for line in file:
        direction, num_steps = line.strip().split(" ")

        moves.append(Move(direction, int(num_steps)))
    
    file.close()

    rope = [Rope_segment() for _ in range(10)]

    for move in moves:
        steps = move.num_steps
        while steps > 0:
            rope[0].move(move.direction)
            for i in range(1, 10):
                if not rope[i].in_range(rope[i - 1]):
                    rope[i].follow(rope[i - 1])
            steps -= 1

    print (len(rope[9].visited_coords))

if __name__ == "__main__":
    main()