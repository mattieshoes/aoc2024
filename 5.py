#!/usr/bin/python3

# validates that a sequence doesn't violate any of the rules in the 
# global before dict
def validate(sequence):
    for b in range(len(sequence)):
        for a in range(b+1, len(sequence)):
            if sequence[b] in before and sequence[a] not in before[sequence[b]]:
                return False
            if sequence[a] in before and sequence[b] in before[sequence[a]]:
                return False
    return True

# corrects a sequence by swapping so it doesn't violate any rules in the
# global before dict
def correct(sequence):
    for b in range(len(sequence)):
        for a in range(b+1, len(sequence)):
            if sequence[b] in before and sequence[a] not in before[sequence[b]]:
                sequence[b], sequence[a] = sequence[a], sequence[b]
            elif sequence[a] in before and sequence[b] in before[sequence[a]]:
                sequence[b], sequence[a] = sequence[a], sequence[b]
    return sequence

with open("inputs/5") as f:
    input = f.read().rstrip("\n").split("\n\n")

# get input data into something more functional -- 2d array with strings to integers
rules = [list(map(int, x.split("|"))) for x in input[0].split("\n")]
sequences = [list(map(int,x.split(","))) for x in input[1].split("\n")]

# build a dictionary out of the rules 
# before[num] contains a set of all numbers it must come before.
before = dict()
for rule in rules:
    if rule[0] in before:
        before[rule[0]].add(rule[1])
    else:
        before[rule[0]] = {rule[1]}

# Validate all sequences, add middle value of valid sequences
part1 = 0
for seq in sequences:
    if validate(seq):
        part1 += seq[len(seq)//2]
print(f"Part 1: {part1}")

# Validate all sequences, throw out valid ones, correct invalid ones, 
# sum new middle value of previously-invalid sequences
part2 = 0
for seq in sequences:
    if not validate(seq):
        new_seq = correct(seq)
        part2 += new_seq[len(new_seq)//2]
print(f"Part 2: {part2}")
