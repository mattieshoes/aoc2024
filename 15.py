#!/usr/bin/python3

# just for debugging
def print_grid():
    for row in grid:
        print(''.join(row))

# checks if there's an immovable obstacle in a given direction
# that could be a wall of a line of boxes with no empty spaces
# checks both halves of boxes moved vertically in part 2

def check_dir(loc, d):
    target = (loc[0]+d[0], loc[1]+d[1])
    v = grid[target[1]][target[0]]
    if v == '.':
        return True
    if v == 'O':
        return check_dir(target, d)
    if v == '[':
        if d[1] != 0: 
            target2 = (loc[0]+d[0]+1, loc[1]+d[1])
            return check_dir(target, d) and check_dir(target2, d)
        else:
            return check_dir(target, d)
    if v == ']':
        if d[1] != 0: # pushing vertically
            target2 = (loc[0]+d[0]-1, loc[1]+d[1])
            return check_dir(target, d) and check_dir(target2, d)
        else:
            return check_dir(target, d)
    return False

# Pushes whatever is in the way in the direction d
# Works for both parts, so [] boxes pushed vertically
# will push things that touch either half of the box

def push(loc, d):
    global grid
    target = (loc[0]+d[0], loc[1]+d[1])
    v = grid[target[1]][target[0]]
    if v == '.':
        grid[target[1]][target[0]] = grid[loc[1]][loc[0]]
        grid[loc[1]][loc[0]] = '.'
    elif v == '[' and d[1] != 0:
        target2 = (loc[0]+d[0]+1, loc[1]+d[1])
        push(target, d)
        push(target2, d)
        grid[target[1]][target[0]] = grid[loc[1]][loc[0]]
        grid[loc[1]][loc[0]] = '.'
    elif v == ']' and d[1] != 0:
        target2 = (loc[0]+d[0]-1, loc[1]+d[1])
        push(target, d)
        push(target2, d)
        grid[target[1]][target[0]] = grid[loc[1]][loc[0]]
        grid[loc[1]][loc[0]] = '.'
    else:
        push(target, d)
        grid[target[1]][target[0]] = grid[loc[1]][loc[0]]
        grid[loc[1]][loc[0]] = '.'

# Checks to see if a move is valid (not smooshing anything into a wall
# then does move

def do_move(d, part2=False):
    global robot_location
    if check_dir(robot_location, d):
        push(robot_location, d)
        robot_location = (robot_location[0]+d[0], robot_location[1]+d[1])

# calculates the score
# works for both part1 and part2
def score():
    s = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == 'O' or grid[y][x] == '[':
                s += 100 * y + x
    return s

with open("inputs/15") as f:
    parts = f.read().rstrip("\n").split("\n\n")

# parse input.  the grid is turned into a 2-D list and the grid
# is turned into (x, y) vectors

grid = [list(x) for x in parts[0].split("\n")]
dirs = {"^": (0, -1), "v": (0, 1), "<": (-1, 0), ">": (1, 0)}
orders = []
for c in parts[1]:
    if c in dirs:
        orders.append(dirs[c])

# Locates the robot, for sanity
robot_location = (0,0)
for y in range(len(grid)):
    for x in range(len(grid[0])):
        if grid[y][x] == '@':
            robot_location = (x, y)
            break
    if robot_location != (0, 0):
        break

# just do the list of orders, calculate score
for o in orders:
    do_move(o)
part1 = score()
print(f"Part 1: {part1}")

# alter the input directly to account for the double-width thing
# Must convert the robot char after empty space char
# then turn back into a grid and find the robot, just like before.
parts[0] = parts[0].replace("#", "##")
parts[0] = parts[0].replace("O", "[]")
parts[0] = parts[0].replace(".", "..")
parts[0] = parts[0].replace("@", "@.")
grid = [list(x) for x in parts[0].split("\n")]
robot_location = (0,0)
for y in range(len(grid)):
    for x in range(len(grid[0])):
        if grid[y][x] == '@':
            robot_location = (x, y)
            break
    if robot_location != (0, 0):
        break

# just do the list of orders, calculate score
for o in orders:
    do_move(o)
part2 = score()
print(f"Part 2: {part2}")
