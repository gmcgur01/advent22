#! /usr/bin/env python3

import sys

def main():

    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <file name>")

    try:
        with open(sys.argv[1]) as file:
            for line in file:
                datastream = line
    except FileNotFoundError:
        sys.exit(f"{sys.argv[1]}: Unable to open file")

    for i in range(14, len(datastream)):
        if check_dupes(datastream[i-14:i]): 
            print(i)
            break

def check_dupes(marker):
    if len(marker) != 14:
        raise Exception("Marker must have a length 4")
    for i in range(14):
        if marker.count(marker[i]) != 1: return False
    return True

if __name__ == "__main__":
    main()