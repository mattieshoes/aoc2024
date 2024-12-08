#!/usr/bin/python3

with open("inputs/8") as f:
    lines = f.read().rstrip("\n").split("\n")
width = len(lines[0])
height = len(lines)

# build dictionary of frequences with a list of transmitters
transmitters = dict()
for row in range(len(lines)):
    for col in range(len(lines[0])):
        frequency = lines[row][col]
        if frequency == '.':
            continue
        if frequency in transmitters:
            transmitters[frequency].append((col,row))
        else:
            transmitters[frequency] = [(col,row)]

# calculate antinodes
# every pair has two
antinodes = set()
for frequency in transmitters:
    for a in range(len(transmitters[frequency])):
        for b in range(a+1, len(transmitters[frequency])):
            A = transmitters[frequency][a]
            B = transmitters[frequency][b]
            deltaX = B[0] - A[0]
            deltaY = B[1] - A[1]
            antinodes.add((B[0]+deltaX, B[1]+deltaY))
            antinodes.add((A[0]-deltaX, A[1]-deltaY))

# Count nodes that are on the grid
part1 = 0
for n in antinodes:
    if 0 <= n[0] < width and 0 <= n[1] < height:
        part1 += 1
print(f"Part 1: {part1}")

# same deal, calculate antinodes, except they repeat.
# repeat until they definitely run off-grid.
# Could be smart about this -- I didn't bother
antinodes = set()
for frequency in transmitters:
    for a in range(len(transmitters[frequency])):
        for b in range(a+1, len(transmitters[frequency])):
            A = transmitters[frequency][a]
            B = transmitters[frequency][b]
            deltaX = B[0] - A[0]
            deltaY = B[1] - A[1]
            for i in range(max(width, height)):
                antinodes.add((B[0] + deltaX * i, B[1] + deltaY * i))
                antinodes.add((A[0] - deltaX * i, A[1] - deltaY * i))

# same deal, sum antinodes that fall on the grid
part2 = 0
for n in antinodes:
    if 0 <= n[0] < width and 0 <= n[1] < height:
        part2 += 1
print(f"Part 2: {part2}")
