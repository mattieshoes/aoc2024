#!/usr/bin/python3

# recursive, depth-first search that takes all valid paths
# returns a dictionary containing the peaks as keys 
# and the number of ways to reach them as values
# This solves part 1 and part 2 simultaneously 

def score(r, c): 
    if lines[r][c] == 9:
        return {(r, c): 1}
    target = lines[r][c] + 1 
    results = dict()
    for off in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            if lines[r+off[0]][c+off[1]] == target:
                temp = score(r+off[0], c+off[1])
                for key in temp.keys():
                    if key in results:
                        results[key] += temp[key]
                    else:
                        results[key] = temp[key]
    return results

with open("inputs/10") as f:
    lines = f.read().rstrip("\n").split("\n")

# Convert chars to ints, and also create a border of -1
# so we don't have to do explicit bounds checking
for i in range(len(lines)):
    lines[i] = [-1] + [int(x) for x in lines[i]] + [-1]
empty = [-1 for x in range(len(lines[0]))]
lines = [empty] + lines + [empty]

# Part 1 is the number of reachable peaks
# Part 2 is the total number of paths (sum of values)
part1 = 0 
part2 = 0 
for r in range(len(lines)):
    for c in range(len(lines[0])):
        if lines[r][c] == 0: # trailhead
            results = score(r, c)
            part1 += len(results)                                                                                                                                                                           
            part2 += sum(results.values())
print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
