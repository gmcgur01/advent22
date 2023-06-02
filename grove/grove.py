#! /usr/bin/env python3
import sys
from collections import deque

def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <file name>")

    try: 
        with open(sys.argv[1]) as file:
            seq = [(i * int(line.rstrip()), int(line.rstrip())) for i, line in enumerate(file)]
    except FileNotFoundError:
        sys.exit(f"{sys.argv[1]}: Unable to open file")

    og_seq = list(seq)
    seq_len = len(seq)
    
    for elem in og_seq:
        move(seq, seq_len, elem)

    zero_index = seq.index((0,0))
    print(seq[(zero_index + 1000) % seq_len][1] + seq[(zero_index + 2000) % seq_len][1] + seq[(zero_index + 3000) % seq_len][1])

def move(list, list_len, elem):
    shift_amount = elem[1] % list_len

    start = list.index(elem)
    end = (start + shift_amount) % list_len

    if elem[1] < 0 and start < end:
        end = (end - 1) % list_len

    if elem[1] > 0 and start > end:
        end = (end + 1) % list_len
    
    if start < end:
        segment = deque(list[start: end + 1])
        segment.rotate(-1)
        for i, val in enumerate(segment, start=start):
            list[i % list_len] = val
    else:
        segment = deque(list[end: start + 1])
        segment.rotate(1)
        for i, val in enumerate(segment, start=end):
            list[i % list_len] = val
     
if __name__ == "__main__":
    main()