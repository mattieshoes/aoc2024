#!/usr/bin/python3

# recursive function that checks if a given starting point and offset will 
# produce the required string.  returns 1 on success, 0 on failure.

def check(x, y, offset, to_match):
    if len(to_match) == 0: # no more letters to match - success
        return 1
    if x < 0 or y < 0 or x >= width or y >= height: # leaves board - fail
        return 0
    if lines[y][x] != to_match[0]: # wrong letter - fail
        return 0
    # good so far, so move x and y according to offset and check next letter
    return check(x+offset[0], y+offset[1], offset, to_match[1:])

with open("inputs/4") as f:
    lines = f.read().rstrip("\n").split("\n")

width = len(lines[0])
height = len(lines)
offsets = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

# brute force every direction from every starting point
part1 = 0
for x in range(width):
    for y in range(height):
        for offset in offsets:
            part1 += check(x, y, offset, "XMAS")
print(f"Part 1: {part1}")

# weirdly easier -- just assume we're at the top-left corner of the X shape
# build the two strings, and see if they say "MAS" or "SAM"
part2 = 0
for x in range(width-2):
    for y in range(height-2):
        a = lines[y][x] + lines[y+1][x+1] + lines[y+2][x+2]
        b = lines[y+2][x] + lines[y+1][x+1] + lines[y][x+2]
        if (a == "MAS" or a == "SAM") and (b == "MAS" or b == "SAM"):
            part2 += 1
print(f"Part 2: {part2}")
