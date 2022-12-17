#! /usr/bin/env python3
import sys


def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <file name>")

    packets = []
    curr_pair = []
    packets.append(curr_pair)

    try:
        with open(sys.argv[1]) as file:
            for line in file:
                line = line.strip()
                if line == "":
                    curr_pair = []
                    packets.append(curr_pair)
                else:
                    curr_pair.append(str_to_list(line))

    except FileNotFoundError:
        sys.exit(f"{sys.argv[1]}: Unable to open file")

    total = 0
    for i in range(len(packets)):
        result = compare_pairs(packets[i][0], packets[i][1])
        if result == True or result == None:
            total += i + 1

    print(total)


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

def compare_pairs(left, right):
    i = 0
    while True:
        if i == len(left) and i == len(right):
            return None
        if i == len(left) or i == len(right):
            return len(left) <= len(right)            
        elif isinstance(left[i], list) and isinstance(right[i], list):
            result = compare_pairs(left[i], right[i])
            if result != None:
                return result
        elif isinstance(left[i], list):
            result = compare_pairs(left[i], [right[i]])
            if result != None:
                return result
        elif isinstance(right[i], list):
            result = compare_pairs([left[i]], right[i])
            if result != None:
                return result
        else:
            if right[i] > left[i]: return True
            if right[i] < left[i]: return False
        i += 1
            

if __name__ == "__main__":
    main()