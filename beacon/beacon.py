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
                sensor, beacon = parse_line(line)
                sensors.append(Sensor(sensor, beacon))

    except FileNotFoundError:
        sys.exit(f"{sys.argv[1]}: Unable to open file")

    left = min(sensors, key=far_left)
    right = max(sensors, key=far_right)


    total = 0
    for i in range(left.sensor.x - left.distance, (right.sensor.x + right.distance) + 1):
        curr_pos = Position(i, 2_000_000)
        is_beacon = False
        for sensor in sensors:
            if curr_pos == sensor.beacon:
                is_beacon = True
        if not is_beacon:
            for sensor in sensors:
                if sensor.in_range(curr_pos):
                    total += 1
                    break

    print(total)


def parse_line(line):
    if matches := re.search(r"Sensor at x=(-*\d+), y=(-*\d+): closest beacon is at x=(-*\d+), y=(-*\d+)", line):
        sensor = Position(int(matches.group(1)), int(matches.group(2)))
        beacon = Position(int(matches.group(3)), int(matches.group(4)))
        return sensor, beacon

@dataclass
class Position:
    x: int
    y: int

class Sensor:
    def __init__(self, sensor, beacon):
        self.sensor = sensor
        self.beacon = beacon
        self.distance = abs(beacon.x - sensor.x) + abs(beacon.y - sensor.y)
    
    def __str__(self):
        return "(" + str(self.sensor) + ", " + str(self.beacon) + ", " + str(self.distance) + ")"

    def in_range(self, pos):
        return abs(self.sensor.x - pos.x) + abs(self.sensor.y - pos.y) <= self.distance

def far_left(sensor):
    return sensor.sensor.x - sensor.distance

def far_right(sensor):
    return sensor.sensor.x + sensor.distance

if __name__ == "__main__":
    main()