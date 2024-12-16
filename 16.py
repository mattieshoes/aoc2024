#!/usr/bin/python3

# Homerolled Dijkstra's algorithm...
#
# A node is a position and a direction we're facing.
# We have a dictionary of solved nodes and frontier nodes
# Key is the node, value is  the score it took to get there
# 
# In our loop, we continually pull the frontier node with the smallest score 
# and expand it.  Expanding it involves:
# 1. move to solved nodes.  Since it has the smallest score among frontier nodes, 
#    nothing is going to get there faster.
# 2. Look at possible moves (turn left, turn right, go forward)
#    1. If that node after a move is already in solved nodes, do nothing
#    2. If that node it encounters is already in frontier nodes,
#       update the score if we just found a better (lower) one.
#    3. If we haven't seen this node before, add it to frontier nodes
#
# When we expand a node on the endpoint of  the maze, we're done

def expand(pos):

    # move from frontier to solved
    solved[pos] = frontier[pos]
    del frontier[pos]

    score = solved[pos]
    x = pos[0]
    y = pos[1]
    facing = pos[2]

    left_move = (x, y, (facing - 1) % 4)
    right_move = (x, y, (facing + 1) % 4)
    forward_move = (x + directions[facing][0], y + directions[facing][1], facing)
    forward_val = grid[forward_move[1]][forward_move[0]]

    if forward_val != '#':
        if forward_move in solved:
            pass
        elif forward_move in frontier:
            if score + 1 < frontier[forward_move]:
                frontier[forward_move] = score + 1
        else:
            frontier[forward_move] = score + 1

    if left_move in solved:
        pass
    elif left_move in frontier:
        if score + 1000 < frontier[left_move]:
            frontier[left_move] = score + 1000
    else:
        frontier[left_move] = score + 1000
    
    if right_move in solved:
        pass
    elif right_move in frontier:
        if score + 1000 < frontier[right_move]:
            frontier[right_move] = score + 1000
    else:
        frontier[right_move] = score + 1000
    return

# Backtrack utilizes the solved nodes dictionary from part 1 to solve part 2.
# Basically we're going backwards, undoing the steps to get here.
# forward is backward, left is right, right is left.
# We know what the score would be for a winning run would be at this point
# just by subtracting, so we can recursively backtrack along all winning paths
# It builds a set of positions (no facing this time, just (x, y)) and the answer
# to part 2 is just the length of that set.

def backtrack(pos):
    global winning_paths
    winning_paths.add((pos[0], pos[1]))

    score = solved[pos]
    x = pos[0]
    y = pos[1]
    facing = pos[2]

    left_move = (x, y, (facing + 1) % 4)
    right_move = (x, y, (facing - 1) % 4)
    forward_move = (x + directions[(facing + 2) % 4][0], y + \
            directions[(facing + 2) % 4][1], facing)
    forward_val = grid[forward_move[1]][forward_move[0]]

    if forward_val != '#':
        if forward_move in solved and solved[forward_move] == score - 1:
            backtrack(forward_move)
   
    if left_move in solved and solved[left_move] == score - 1000:
        backtrack(left_move)
    
    if right_move in solved and solved[right_move] == score - 1000:
        backtrack(right_move)
    return


with open("inputs/16") as f:
    grid = f.read().rstrip("\n").split("\n")

# rather than store the direction we're facing as a tuple, I will just store
# the index of the directions list.  so turning right is (facing+1)%4 and 
# turning left is (facing-1)%4.  Easy peasy.

start = (0, 0)
end = (0, 0)
directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
facing = directions[1]
for y in range(len(grid)):
    for x in range(len(grid[0])):
        if grid[y][x] == 'S':
            start = (x, y)
        elif grid[y][x] == 'E':
            end = (x, y)

# home rolled Dijkstra's algorithm
# explained with the expand function above

part1 = 0
part1_key = ''
solved = dict()
frontier = {(start[0], start[1], 1): 0}
win_condition = {(end[0], end[1], 0), (end[0], end[1], 1), \
        (end[0], end[1], 2), (end[0], end[1], 3)}

while len(frontier) > 0:
    # find smallest score in frontier nodes
    smallest = 999999999
    smallest_key = ''
    for k in frontier.keys():
        if frontier[k] < smallest:
            smallest = frontier[k]
            smallest_key = k

    if part1 > 0 and smallest > part1:
        break

    # expand that node
    expand(smallest_key)

    # Repeat until we happened to have just solved
    # the node at the end of the maze.  
    if smallest_key in win_condition:
        part1 = solved[smallest_key]
        part1_key = smallest_key
print(f"Part 1: {part1}")

# using part1 solved nodes set to backtrack through all winning paths
winning_paths = set()
for wc in win_condition:
    if wc in solved:
        backtrack(wc)
part2 = len(winning_paths)
print(f"Part 2: {part2}")

