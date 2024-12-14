#!/usr/bin/python3

import re
from math import prod

# Prints grid
def printgrid():
    for row in range(height):
        for col in range(width):
            count = 0
            for b in bots:
                if b[0] == col and b[1] == row:
                    count += 1
            if count == 0:
                print(".", end="")
            else:
                print(count, end="")
        print()

# returns quadrant bot is in
# 0 for no quadrant
def safety_score():
    counts = [0, 0, 0, 0]
    for bot in bots:
        for i in range(len(quadrants)):
            if bot[0] >= quadrants[i][0] and bot[0] < quadrants[i][2] and \
                    bot[1] >= quadrants[i][1] and bot[1] < quadrants[i][3]:
                counts[i] += 1
                break
    return prod(counts)

# iterates global bots list 'steps' steps.
def iterate(steps):
    for i in range(len(bots)):
        bots[i] = [(bots[i][0] + bots[i][2] * steps) % width, \
                   (bots[i][1] + bots[i][3] * steps) % height, \
                   bots[i][2], bots[i][3]]

with open("inputs/14") as f:
    lines = f.read().rstrip("\n").split("\n")

height = 103
width = 101
quadrants = [(0, 0, width//2, height//2), (width//2+1, 0, width, height//2), (0, height//2+1, width//2, height), (width//2+1, height//2+1, width, height)]

bots = []
for line in lines:
    result = [int(x) for x in re.findall('[0-9-]+', line)]
    bots.append(result)

iterate(100)
part1 = safety_score()
print(f"Part 1: {part1}")

# Assumption: a picture of a christmas tree will be centered, with a boatload
# of bots in the middle column.  This means probably an abnormally low
# safety score.  Also explains why part 1 has the whole safety score thing.
# This just prints the grid whenever a new lowest safety score is found
iterate(-100) # iterate works in reverse!
best = 999999999
part2 = 0
for count in range(101*103):
    counts = [0,0,0,0,0]
    score = safety_score()
    if score < best:
        best = score
        #printgrid()
        #print(count)
        part2 = count
    iterate(1)
print(f"Part 2: {part2}")

