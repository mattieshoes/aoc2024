#!/usr/bin/python3

# edges be like
# ((1,0), 4, 3, 6)
# - (1,0) being direction (to the right)
# - 4 being the X value that this right-hand fence is sitting on
# - 3 being the starting Y value
# - 6 being the ending Y value
# so there's a vertical fence at (4,3), (4,4), (4,5)
# if it was a horizontal fence, then the 4 would be a Y value, 
# and 3 and 6 would be X values.
# combine just looks at edges and see if they line up.
# that is, same direction, same coordinate, and one starts where the other ends
# recursive function was mostly to avoid the sets changing during loops.

def combine(edges):
    for a in edges:
        for b in edges:
            if a[0] == b[0] and a[1] == b[1] and a[3] == b[2]:
                edges.add((a[0], a[1], a[2], b[3]))
                edges.remove(a)
                edges.remove(b)
                return(combine(edges))
    return edges

# given the set of positions included in the shape, this identifies the sides
# and creates edges to feed to the combine function
# then it returns the combined sides.  Strictly speaking, it could just return
# the count of sides since that's all we need, but whatever.

def get_sides(shape):
    verticals = set()
    horizontals = set()

    for pos in shape:
        for offset in [(-1, 0), (1, 0)]:
            target = (pos[0] + offset[0], pos[1] + offset[1])
            if target not in shape: # edge
                verticals.add((offset, pos[0], pos[1], pos[1]+1))
        for offset in [(0, -1), (0, 1)]:
            target = (pos[0] + offset[0], pos[1] + offset[1])
            if target not in shape: # edge
                horizontals.add((offset, pos[1], pos[0], pos[0]+1))
    verticals = combine(verticals)
    horizontals = combine(horizontals)
    return verticals | horizontals

# This calculates contiguous sections recursively and avoid duplicating by passing
# around sets of already-checked coordinates.  
# It calculates perimeters as well fort part 1.

def section(pos, already_checked):
    perimeter = 0
    already_checked.add(pos)

    for offset in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        target = (pos[0] + offset[0], pos[1] + offset[1])
        if target not in already_checked:
            if lines[pos[1]][pos[0]] == lines[target[1]][target[0]]:
                (new_already_checked, new_perimeter) = section(target, already_checked)
                already_checked = new_already_checked
                perimeter += new_perimeter
            else:
                perimeter += 1
    return (already_checked, perimeter)

with open("inputs/12") as f:
    lines = f.read().rstrip("\n").split("\n")

# Build grid with a border of '0' squares to avoid edge detection 
# then we just ignore the '0' section when calculating
for i in range(len(lines)):
    lines[i] = ['0'] + list(lines[i]) + ['0']
empty = ['0' for x in range(len(lines[0]))]
lines = [empty] + lines + [empty]

# goes and finds all sections using section.
# keeps track of positions already part of a section so we dont' double-count
# gets area and perimeter directly from the section function
# for part 2, it takes the set of positions in the section and finds edges
# with get_sides function.  The get_sides function stitches the sides together
# so we just get total number of sides

checked = set()
part1 = 0
part2 = 0
for y in range(len(lines)):
    for x in range(len(lines[0])):
        if lines[y][x] != '0' and (x, y) not in checked:
            (area_set, perimeter) = section((x, y), set())
            area = len(area_set)
            part1 += area * perimeter
            part2 += area * len(get_sides(area_set))
            checked = checked | area_set
print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
