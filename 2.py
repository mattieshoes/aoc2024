#!/usr/bin/python3

# Verfies sequence is always increasing or always decreasing
# and every step is no more than 3

def is_safe(report):
    inc = False
    dec = False

    for pair in zip(report[:-1], report[1:]):
        if pair[0] == pair[1]:
            return False
        if pair[0] > pair[1]:
            dec = True
        else:
            inc = True
        if inc and dec:
            return False
        if abs(pair[0]-pair[1]) > 3:
            return False
    return True

# if the sequence isn't safe, try each sequence created by skipping an
# element in the sequence.

def damper(report):
    if is_safe(report):
        return True
    for i in range(len(report)):
        if is_safe(report[:i] + report[i+1:]):
            return True
    return False

# Get inputs

with open("inputs/2") as f:
    lines = f.read().rstrip("\n").split("\n")

# Parse inputs and check safety, give count
part1 = 0
for line in lines:
    if is_safe(list(map(int, line.split()))):
        part1 += 1
print(f"Part 1: {part1}")

# Parse inputs and check safety with the damper, give count
# Probably should have parsed inputs only once
part2 = 0
for line in lines:
    if damper(list(map(int, line.split()))):
        part2 += 1
print(f"Part 2: {part2}")
