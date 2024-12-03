#!/usr/bin/python3

import re

with open("inputs/3") as f:
    input = f.read()

# regex will match mul(num1,num2) where num1 and num2 are 1-3 digit strings
# and output a list of tuples.  ie. 
# [('<num1>', '<num2>'), ('<num1>', '<num2>'), ...]

pattern = "mul\((\d{1,3}),(\d{1,3})\)"
match_list = re.findall(pattern, input)

# iterate through tuples, converting strings to ints, multiplying them, 
# then summing the results

part1 = 0
for m in match_list:
    part1 += int(m[0]) * int(m[1])
print(f"Part 1: {part1}")

# regex
# will catch the above as well as do() and don't(), returning a list of tuples.  
# Might be:
# ('<num1>', '<num2>', '', '')
# ('', '', 'do', '')
# ('', '', '', "don't")

pattern = "mul\((\d{1,3}),(\d{1,3})\)|(do)\(\)|(don't)\(\)"
match_list = re.findall(pattern, input)

# iterate through tuples tracking state of do vs don't, and summing the product 
# of the numbers when the state is true

do = True
part2 = 0
for m in match_list:
    if m[2] == "do":
        do = True
    elif m[3] == "don't":
        do = False
    elif do:
        part2 += int(m[0]) * int(m[1])
print(f"Part 2: {part2}")
