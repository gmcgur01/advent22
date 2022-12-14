#! /usr/bin/env python3
import sys


def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <file name>")

    packets = []
    curr_pair = []

    try:
        with open(sys.argv[1]) as file:

            for line in file:
                line = line.strip()
                if line == "":
                    packets.append(curr_pair)
                    curr_pair = []
                else:
                    curr_pair.append(str_to_list(line))

    except FileNotFoundError:
        sys.exit(f"{sys.argv[1]}: Unable to open file")

    for pair in packets:
        print(pair[0])
    
    print("hello world")

def str_to_list(line):
    list_levels = []
    ret = None
    i = 0
    while i < len(line):
        if line[i] == "[":
            new_list = []
            if len(list_levels) == 0:
                ret = new_list
                list_levels.append(ret)
            else:
                list_levels[len(list_levels) - 1].append(new_list)
                list_levels.append(new_list)
        elif line[i] == "]":
            list_levels.pop()
        elif line[i] == ",":
            i += 1
            continue
        else:
            num = int(line[i])
            i += 1
            while line[i] != "[" and line[i] != "]" and line[i] != ",":
                num = (num * 10) + int(line[i])
                i += 1
            list_levels[len(list_levels) - 1].append(num)
            continue
        i += 1
    return ret

if __name__ == "__main__":
    main()