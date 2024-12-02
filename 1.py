#!/usr/bin/python3

with open("inputs/1") as f:
    lines = f.read().rstrip("\n").split("\n")

left = list()
right = list()

for line in lines:
    fields = line.split()
    left.append(int(fields[0]))
    right.append(int(fields[1]))

left.sort()
right.sort()

part1 = 0
for pair in zip(left, right):
    part1 += abs(pair[0] - pair[1])
print(f"Part 1: {part1}")

part2 = 0
for num in left:
    part2 += num * right.count(num)
print(f"Part 2: {part2}")