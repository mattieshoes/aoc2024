#!/usr/bin/python3

import re
from itertools import count
from math import lcm

# OMFG
# Part 2 solution.  It's not perfect (it can't solve part 1) probably 
# because the cycle finding overruns the actual answer.  That's not
# an issue with part 2 since the prize is out past 10 trillion

def solve2(a, b, prize):

    # find the X cycle and X offset for a (where mod b will be 0)
    x_set = set()
    x_cycle = 0
    x_offset = 0
    for i in range(b[0]+1):
        x_res = (prize[0] - a[0] * i) % b[0]
        if x_res in x_set:
            x_cycle = len(x_set)
            break
        if x_res == 0:
            x_offset = len(x_set)
        x_set.add(x_res)

    # find the Y cycle and Y offset for a (where % b will be 0)
    y_set = set()
    y_cycle = 0
    y_offset = 0
    for i in range(b[1]+1):
        y_res = (prize[1] - a[1] * i) % b[1]
        if y_res in y_set:
            y_cycle = len(y_set)
            break
        if y_res == 0:
            y_offset = len(y_set)
        y_set.add(y_res)

    # the cycle length for A will be the LCM of the X and Y cycle
    a_cycle = lcm(x_cycle, y_cycle)
    a_offset = 0

    # That A cycle will be offset by some number of X cycles  
    # There must be a clever way to find that, but I don't know
    # 
    # First offset by the X cycle offset, then run through X 
    # cycles until Y works, to get the offset for A cycles
    target = (prize[0] - a[0] * x_offset, prize[1] - a[1] * x_offset)
    remainders = set()
    for i in count():
        if target[1] % b[1] == 0:
            a_offset = i * x_cycle + x_offset
            break
        remainder = target[1] % b[1]
        if remainder in remainders:
            return 0
        remainders.add(target[1] % b[1])
        target = (target[0] - a[0] * x_cycle, target[1] - a[1] * x_cycle)


    # Okay, so press A a_offset times so get the Y values divisble for B
    # then look at how far Y is off if we press B enough to make X = 0

    target = (prize[0] - a[0] * a_offset, prize[1] - a[1] * a_offset)
    b_press = target[0] // b[0]
    yr1 = target[1] - b_press * b[1]
    
    # then iterate forwards one a_cycle and do it again.
    target = (target[0] - a[0] * a_cycle, target[1] - a[1] * a_cycle)
    b_press = target[0] // b[0]
    yr2 = target[1] - b_press * b[1]

    # Subtracing them will tell us 
    ydiff = yr2-yr1

    # 1. Whether Y is approaching zero
    # if not, no solution
    if abs(yr2) > abs(yr1):
        return 0

    # 2. Whether it will hit zero or skip over it.
    # if it will skip over zero, there's no solution
    if yr1 % ydiff != 0:
        return 0

    # 3. How many a_cycles we'll need to run to get X
    # and y to zero at the same time.
    cycles = abs(yr1 // ydiff)

    # So we start with prize
    # press A a_offset times to get us to the part of a_cycle where 
    # remainders are zero, then do 'a_cycle' presses 'cycles' times
    # so B presses will zero out X and Y at the same time
    a_presses = a_offset + a_cycle * cycles

    # and from there, we can calculate b_presses from what's left
    target = (prize[0] - a[0] * a_presses, prize[1] - a[1] * a_presses)
    b_presses = target[0] // b[0]

    return a_presses * 3 + b_presses

# Naive solution for part 1
def solve(a, b, prize):
    best = 0
    for a_presses in count():
        left = (prize[0] - a[0]*a_presses, prize[1] - a[1]*a_presses)
        if left[0] < 0 or left[1] < 0:
            break
        if left[0] % b[0] == 0 and left[1] % b[1] == 0 and left[0] // b[0] == left[1] // b[1]:
            result = a_presses * 3 + left[0] // b[0]
            if result < best or best == 0:
                best = result
    return best


with open("inputs/13") as f:
    parts = f.read().rstrip("\n").split("\n\n")

part1 = 0
part2 = 0
for part in parts:
    result = re.findall("\d+", part)
    a = (int(result[0]), int(result[1]))
    b = (int(result[2]), int(result[3]))
    prize = (int(result[4]), int(result[5]))
    part1 += solve(a, b, prize)
    prize = (prize[0] + 10000000000000, prize[1] + 10000000000000)
    result = solve2(a, b, prize)
    part2 += solve2(a, b, prize)

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
