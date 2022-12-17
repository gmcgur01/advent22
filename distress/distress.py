#! /usr/bin/env python3
import sys


def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <file name>")

    packets = []

    try:
        with open(sys.argv[1]) as file:
            for line in file:
                line = line.strip()
                if line != "":
                    packets.append(Packet(line))

    except FileNotFoundError:
        sys.exit(f"{sys.argv[1]}: Unable to open file")

    div1 = Packet([[2]])
    div2 = Packet([[6]])

    packets.append(div1)
    packets.append(div2)
    packets.sort()

    decoder_key = (packets.index(div1) + 1) * (packets.index(div2) + 1)
    print(decoder_key)

class Packet:
    
    def __init__(self, data):
        if isinstance(data, str):
            self.data = str_to_list(data)
        else:
            self.data = data
    def __eq__(self, other):
        return compare_pairs(self.data, other.data) == None

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return compare_pairs(self.data, other.data) == True

    def __rt__(self, other):
        return compare_pairs(self.data, other.data) == False

    def __ge__(self, other):
        result = compare_pairs(self.data, other.data)
        return result == False or result == None

    def __le__(self, other):
        result = compare_pairs(self.data, other.data)
        return result == True or result == None

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