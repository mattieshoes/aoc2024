#!/usr/bin/python3

# For part 2 -- recursive function finding all uniqe trails
# returns number
def alternative_score(r, c):
    if lines[r][c] == 9:
        return 1
    target = lines[r][c] + 1
    results = 0
    for off in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            if lines[r+off[0]][c+off[1]] == target:
                results += alternative_score(r+off[0], c+off[1])
    return results

# For part 1 -- recursive function finding reachable peaks
# returns set containing reachable peaks to avoid duplicates
def score(r, c):
    if lines[r][c] == 9:
        return {(r, c)}
    target = lines[r][c] + 1
    results = set()
    for off in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            if lines[r+off[0]][c+off[1]] == target:
                results.update(score(r+off[0], c+off[1]))
    return results

with open("inputs/10") as f:
    lines = f.read().rstrip("\n").split("\n")

# Convert chars to ints, and also create a border of -1
# so we don't have to do explicit bounds checking
for i in range(len(lines)):
    lines[i] = [-1] + [int(x) for x in lines[i]] + [-1]
empty = [-1 for x in range(len(lines[0]))]
lines = [empty] + lines + [empty]

# just sum number of reachable peaks for each trailhead
part1 = 0
for r in range(len(lines)):
    for c in range(len(lines[0])):
        if lines[r][c] == 0: # trailhead
            part1 += len(score(r, c))
print(f"Part 1: {part1}")

# just sum number of unique trails for each trailhead
part2 = 0
for r in range(len(lines)):
    for c in range(len(lines[0])):
        if lines[r][c] == 0: # trailhead
            part2 += alternative_score(r, c)
print(f"Part 2: {part2}")
