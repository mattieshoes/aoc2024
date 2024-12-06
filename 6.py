#!/usr/bin/python3

# Returns true if location is on the grid, false otherwise.
def on_grid(location):
    if location[0] >= 0 and location[1] >= 0 and \
       location[0] < len(lines) and location[1] < len(lines[0]):
        return True
    return False

# Moves our soldier forward, or turns right if blocked.
def iterate():
    global pos, facing
    in_front = (pos[0]+facing[0], pos[1]+facing[1])
    if on_grid(in_front) and  lines[in_front[0]][in_front[1]] == '#':
            facing = (facing[1], -1*facing[0])
            return
    pos = in_front

with open("inputs/6") as f:
    lines = f.read().rstrip("\n").split("\n")

# locate starting position and direction of travel
starting_pos = (0, 0)
starting_facing = (0, 0)
for r in range(len(lines)):
    for c in range(len(lines[0])):
        if lines[r][c] != '.' and lines[r][c] != '#':
            starting_pos = (r, c)
            if lines[r][c] == '^':
                starting_facing = (-1, 0)
            elif lines[r][c] == '>':
                starting_facing = (0, 1)
            elif lines[r][c] == '<':
                starting_facing = (0, -1)
            elif lines[r][c] == 'v':
                starting_facing = (1, 0)
            break

# Iterate our soldier until he leaves the board.  Count number of uniqe locations
pos = starting_pos
facing = starting_facing
locs = set()
while on_grid(pos):
    locs.add(pos)
    iterate()
part1 = len(locs)
print(f"Part 1: {part1}")

# In order to affect our soldier's path, we must place an obstacle somewhere 
# in his path from part 1
# Just step through the set, flipping an empty non-starting space to an 
# obstacle, then iterate our soldier until he either leaves the grid or hits
# the same grid square with the same direction of travel 
# (ie. caught in a loop)

# convert strings to char arrays so we can muck with them
for r in range(len(lines)):
    lines[r] = list(lines[r])

to_test = locs
to_test.remove(starting_pos)

part2 = 0
for p in to_test:
    lines[p[0]][p[1]] = '#'
    pos = starting_pos
    facing = starting_facing
    locs = set()
    while on_grid(pos):
        full_loc = (pos[0], pos[1], facing[0], facing[1])
        if full_loc in locs: # loop
            part2 += 1
            break
        locs.add(full_loc)
        iterate()
    lines[p[0]][p[1]] = '.'
print(f"Part 2: {part2}")
