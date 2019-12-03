#!/usr/bin/env python3

import sys


def draw_wires(coord1, coord2):
    xmax = max(val[0] for val in coord1|coord2)
    xmin = min(val[0] for val in coord1|coord2)
    ymax = max(val[1] for val in coord1|coord2)
    ymin = min(val[1] for val in coord1|coord2)

    for x in range(xmin, xmax+1):
        outline = ''
        for y in range(ymin, ymax+1):
            if (x,y) in coord1 and (x,y) in coord2:
                outline += 'X'
            elif (x,y) in coord1:
                outline += '1'
            elif (x,y) in coord2:
                outline += '2'
            else:
                outline += '.'
    print(outline)


def coord_set(instring):
    steps = 0
    coords = set()
    values = instring.split(',')
    current = (0,0)
    for value in values:
        direction = value[0]
        distance = int(value[1:])
        if direction == 'U':
            for i in range(current[1]+1, current[1]+distance+1):
                steps += 1
                coords.add((current[0], i, steps))
            current = (current[0], current[1]+distance)
        elif direction == 'D':
            for i in range(current[1]-1, current[1]-distance-1, -1):
                steps += 1
                coords.add((current[0], i, steps))
            current = (current[0], current[1]-distance)
        elif direction == 'L':
            for i in range(current[0]-1, current[0]-distance-1, -1):
                steps += 1
                coords.add((i, current[1], steps))
            current = (current[0]-distance, current[1])
        elif direction == 'R':
            for i in range(current[0]+1, current[0]+distance+1):
                steps += 1
                coords.add((i, current[1], steps))
            current = (current[0]+distance, current[1])
    return coords


with open(sys.argv[1]) as infile:
    first, second = infile.read().strip().split('\n')

coord1 = coord_set(first)
coord2 = coord_set(second)

intersections = {(val[0], val[1]) for val in coord1} & {(val[0], val[1]) for val in coord2}
best = float('inf')
for intersection in intersections:
    dist = abs(intersection[0])+abs(intersection[1])
    if best > dist:
        best = dist

print(f'Part a: {best}')

lookup1 = {(val[0], val[1]): val[2] for val in coord1}
lookup2 = {(val[0], val[1]): val[2] for val in coord2}
intersections = {(val[0], val[1]) for val in coord1} & {(val[0], val[1]) for val in coord2}
best = float('inf')
for intersection in intersections:
    dist = lookup1[intersection] + lookup2[intersection]
    if best > dist:
        best = dist

print(f'Part b: {best}')
