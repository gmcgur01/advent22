#! /usr/bin/env python3
import sys
import re
from dataclasses import dataclass

def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <file name>")

    sensors = []

    try:
        with open(sys.argv[1]) as file:
            for line in file:
                line = line.strip()
                sensor = parse_line(line)
                sensors.append(sensor)

    except FileNotFoundError:
        sys.exit(f"{sys.argv[1]}: Unable to open file")

    
    for i in range(4000001):
        ranges = []
        for sensor in sensors:
            interval = sensor.get_range(i)
            if interval != None: ranges.append(interval)
        ranges.sort(key=get_start)
        farthest_right = 0
        for j in range(len(ranges) - 1):
            if ranges[j][1] > farthest_right: 
                farthest_right = ranges[j][1]
            if farthest_right - ranges[j+1][0] < -1:
                print((farthest_right + 1) * 4000000 + i)
                return

def parse_line(line):
    if matches := re.search(r"Sensor at x=(-*\d+), y=(-*\d+): closest beacon is at x=(-*\d+), y=(-*\d+)", line):
        sensor_x = int(matches.group(1))
        sensor_y = int(matches.group(2))
        beacon_x = int(matches.group(3))
        beacon_y = int(matches.group(4))
        range = abs(beacon_x - sensor_x) + abs(beacon_y - sensor_y)
        return Sensor(sensor_x, sensor_y, range)

class Sensor:
    def __init__(self, sensor_x, sensor_y, range):
        self.x = sensor_x
        self.y = sensor_y
        self.range = range
    
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ", " + str(self.range) + ")"

    def get_range(self, y):
        y_diff = abs(y - self.y)
        if y_diff > self.range:
            return None
        return (self.x - (self.range - y_diff)), (self.x + (self.range - y_diff))

    def in_range(self, x, y):
        return abs(self.x - x) + abs(self.y - y) <= self.range

def get_start(range):
    return range[0]

def get_end(range):
    return range[1]

if __name__ == "__main__":
    main()