#!/usr/bin/python3

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

def damper(report):
    if is_safe(report):
        return True
    for i in range(len(report)):
        if is_safe(report[:i] + report[i+1:]):
            return True
    return False

with open("inputs/2") as f:
    lines = f.read().rstrip("\n").split("\n")

part1 = 0
for line in lines:
    if is_safe(list(map(int, line.split()))):
        part1 += 1
print(f"Part 1: {part1}")

part2 = 0
for line in lines:
    if damper(list(map(int, line.split()))):
        part2 += 1
print(f"Part 2: {part2}")