#!/usr/bin/python3

import functools

# Since stones never combine when we blink, we can iterate each value 
# separately.  Since there's a lot of repeat combinations of a value and 
# a number of blinks, we can cache prior results what happens rather than 
# make the same calculations incessantly -- the term is memoization.  
# Python's functools library  has some built in memoization stuff for 
# functions that don't rely on external data like globals
# So we can just import functools, use the @functools.cache decorator, 
# and it just automatically caches prior results and uses them when
# it gets the same inputs.
# 
# The function itself just returns how many values it  has.  At the 
# leaves of our search tree, that's always going to be 1. On the 
# interior nodes of the tree, it's going to be a sum of the branches

@functools.cache
def iterate(val, times):
    if times == 0:
        return 1
    strval = str(val)
    if val == 0:
        return iterate(1, times - 1)
    elif len(strval) % 2 == 0:
        return iterate(int(strval[len(strval)//2:]), times - 1) + iterate(int(strval[:len(strval)//2]), times - 1)
    return iterate(val*2024, times-1)
    
with open("inputs/11") as f:
    line = f.read().rstrip("\n").split(" ")
values = [int(x) for x in line]

part1 = 0
for val in values:
    part1 += iterate(val, 25)
print(f"Part 1: {part1}")

part2 = 0
for val in values:
    part2 += iterate(val, 75)
print(f"Part 2: {part2}")
