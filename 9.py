#!/usr/bin/python3

# Looks for the next file to move,looking right-to-left, starting from 
# start_location, so we don't have to continually scan the empty space on the
# right
#
# Could cache this while building layout, but whatever, tired
# It ignores files we already moved or failed to move

def last_file_id_location_size(start_location, ignore):
    for i in range(start_location, 0, -1):
        if layout[i] < 0: # empty space
            continue
        if layout[i] in ignore: # a file we already failed to move
            continue
        file_end = i
        file_id = layout[i]
        for j in range(i-1, 0, -1):
            if layout[j] != file_id:
                return((file_id, j+1, i-j))
    return (-1, -1, -1)

# Looks for contiguous space of `size` before the start of the 
# file we're trying to move. Also returns the index of the first empty cell
# so we can start future searches from there in the future, not looking at 
# all the filled-up space on the left.
# 
# Could also be cached when building the layout
# in fact, could probably ditch the actual layout entirely by 
# keeping a sorted list of empty contiguous space and 
# file id/location/size, but it's late and this works.

def find_empty_space(start_search, size, end_search):
    state = 0
    empty_size = 1
    first_empty = end_search
    for i in range(start_search, end_search, 1):
        if state == 0: # searching
            if layout[i] == -1:
                state = 1
                first_empty = min(i, first_empty)
                empty_start = i
        elif state == 1: # in empty space, looking for size
            if layout[i] > 0:
                empty_size = i - empty_start
                if empty_size >= size:
                    return (first_empty, empty_start)
                state = 0
    return (first_empty, -1)

# turns input string into a list of actual drive contents
# each cell of the layout holds the file_id, or -1 for empty.

def build_drive_layout():
    global layout
    layout = []
    file_id = 0
    for index in range(0, len(line), 2):
        a = int(line[index])
        for i in range(a):
            layout.append(file_id)
        file_id += 1
        if index+1 < len(line):
            b = int(line[index+1])
            for i in range(b):
                layout.append(-1)

with open("inputs/9") as f:
    line = f.read().rstrip("\n")

build_drive_layout()

# two indexes
# blank moves right holding the index of the next blank sector
# data moves left holding the index of the last non-blank sector
# swaps the contents, updates the indexes
# when they cross, the data is all smooshed to the left
blank = 0
while layout[blank] >= 0:
    blank += 1
data = len(layout)-1
while layout[data] < 0:
    data -= 1
while blank < data:
    layout[blank] = layout[data]
    layout[data] = -1;
    while layout[blank] >= 0:
        blank += 1
    while layout[data] < 0:
        data -= 1

# Calculate the "checksum"
part1 = 0
for i in range(blank):
    part1 += layout[i] * i
print(f"Part 1: {part1}")

# Part 2 -- same schema as before, but we only move entire files
# so we search for the last file on disk that we haven't already effed with
# if we find no file_id (return value -1), we're done.
# Then we look for contiguous space for the file starting from the left
# we keep track of the first empty space on the drive and the location of the 
# last file we tried to move, so we don't keep re-scanning the "solved" parts
# of the "drive"
# uses empty_loc of -1 to indicate nowhere to move it
# swip swap
# add to the set of files we've already moved so we don't try moving them 
# later
# repeat until no more files to try and mush left.

build_drive_layout()
ignore = set()
location = len(layout)
first_empty = 0
while True:
    (file_id, location, size) = last_file_id_location_size(location-1, ignore) 
    if file_id == -1: # no more files to try moving
        break
    (first_empty, empty_loc) = find_empty_space(first_empty, size, location+1)
    if empty_loc == -1: # nowhere to move it
        continue

    for i in range(size):
        layout[empty_loc + i] = file_id
        layout[location + i] = -1
    ignore.add(file_id) # so we don't try re-moving it later.

# Same "checksum" stuff
part2 = 0
for i in range(len(layout)):
    if layout[i] >= 0:
        part2 += i * layout[i]
print(f"Part 2: {part2}")
