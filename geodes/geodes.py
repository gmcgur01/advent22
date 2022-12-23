#! /usr/bin/env python3
import sys

def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <file name>")

    try:
        with open(sys.argv[1]) as file:
            blueprints = [line.strip() for line in file]
    except FileNotFoundError:
        sys.exit(f"{sys.argv[1]}: Unable to open file")

    print(blueprints)

if __name__ == "__main__":
    main()