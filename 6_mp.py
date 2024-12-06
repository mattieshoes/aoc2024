#!/usr/bin/python3

import concurrent.futures

# Turns direction to the right, just for clarity
# seems backwards because our Y axis is flipped -- "down" is increasing values
def turn_right(direction):
    return direction * (0+1j)

# Moves our guard forward as far forward as possible before hitting
# an obstacle or moving off-grid.  returns resulting position
def iterate(grid, pos, facing, spot): 
    target = pos + facing
    while target in grid and grid[target] != '#' and target != spot:
        target += facing
    if target in grid: # We hit an obstacle
        return target - facing
    else: # we went off-grid
        return target

with open("inputs/6") as f:
    lines = f.read().rstrip("\n").split("\n")

# Turn our input into a dictionary indexed by complex numbers
# the X position being real, Y being imaginary.
# it's somewhat backwards because Y values increase when going "down"
# using complex numbers allows for a single index for each position 
# on the board.  As a side benefit, bounds checking becomes just checking
# if a key is in our dictionary.
#
# While we're at it, identify the starting position and direction

grid = dict()
starting_pos = 0+0j
starting_facing = 0
for i in range(len(lines)):
    for r in range(len(lines[0])):
        index = complex(r, i)
        grid[index] = lines[i][r]
        if lines[i][r] != '.' and lines[i][r] != '#':
            starting_pos = index
            dirs = {'^': 0-1j, '>': 1+0j, 'v': 0+1j, '<': -1+0j}
            starting_facing = dirs[lines[i][r]]

# Simulate soldier movement and turning, count unique squares
pos = starting_pos
facing = starting_facing
visited = set()
while pos in grid:
    visited.add(pos)
    target = pos+facing
    if target in grid and grid[target] == '#':
        facing = turn_right(facing)
    else:
        pos = target
part1 = len(visited)
print(f"Part 1: {part1}")

# In order to affect our soldier's path, we must place an obstacle somewhere 
# in his path from part 1, ignoring his starting position
# Just step through the set, placing obstacles, detecting loops, and then
# removing the obstacles
#
# Loop detection is just checking whether we've been at this location facing 
# the same direction.

def check(spot):
    pos = starting_pos
    facing = starting_facing
    locs = set()
    while pos in grid:
        if (pos, facing) in locs: # loop
            return 1
        locs.add((pos, facing))
        pos = iterate(grid, pos, facing, spot)
        facing = turn_right(facing)
    return 0

part2 = 0
visited.remove(starting_pos)
with concurrent.futures.ProcessPoolExecutor(max_workers = 4) as executor:
    results = executor.map(check, visited)
part2 = sum(results)
print(f"Part 2: {part2}")
