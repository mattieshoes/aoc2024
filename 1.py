#!/usr/bin/python3

# get inputs
with open("inputs/1") as f:
    lines = f.read().rstrip("\n").split("\n")

# parse inputs -- columns to rows, strings to ints
left = list()
right = list()
for line in lines:
    fields = line.split()
    left.append(int(fields[0]))
    right.append(int(fields[1]))

# sort and sum the absolute value of the differences
left.sort()
right.sort()
part1 = 0
for pair in zip(left, right):
    part1 += abs(pair[0] - pair[1])
print(f"Part 1: {part1}")

# The "right" way is probably to make a dictionary if we were going
# to refer back to this a lot, but we aren't, so simply counting
# instances in the right column works fine
part2 = 0
for num in left:
    part2 += num * right.count(num)
print(f"Part 2: {part2}")
