import sys
from dataclasses import dataclass

@dataclass(frozen=True)
class Operation:
    type: str
    num: int 

    def get_cycles(self):
        match self.type:
            case "noop":
                return 1
            case "addx":
                return 2
            case _:
                raise ValueError("Invalid op type")

def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage: python3 {sys.argv[0]} <file name>")
    
    ops = []

    try:
        with open(sys.argv[1]) as file:
            for line in file: 
                line = line.strip()
                if line == "noop":
                    ops.append(Operation("noop", 0))
                else:
                    type, value = line.split(" ")
                    ops.append(Operation(type, int(value)))
    except FileNotFoundError:
        sys.exit(f"Unable to open: {sys.argv[1]}")

    curr_value = 1
    value_list = []

    for op in ops:
        cycles = op.get_cycles()
        while cycles > 0:
            value_list.append(curr_value)
            cycles -= 1
        curr_value += op.num
    value_list.append(curr_value)
            
    screen = [[" " for _ in range(40)] for _ in range(6)]

    for row_num in range(6):
        for col_num in range(40):
            pixel_num = 40 * row_num + col_num
            if abs((pixel_num % 40) - value_list[pixel_num]) <= 1:
                screen[row_num][col_num] = "#"

    for row in screen:
        for pixel in row:
            print(pixel, end="")
        print("")
    
if __name__ == "__main__":
    main()