#!/usr/bin/env python3

import sys


def calc_tot_dist(goal, coords, max_dist):
    tot_dist = 0
    for coord in coords:
        tot_dist += abs(coord[0]-goal[0]) + abs(coord[1]-goal[1])
        if tot_dist >= max_dist:
            break
    return tot_dist


def test_dist():
    coords = [(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)]

    assert calc_max_area(coords, max_dist=32) == 16


def calc_max_area(coords, max_dist=10000):
    coords.sort()
    board_max = (max(i[0] for i in coords), max(i[1] for i in coords))
    ok = 0
    for i in range(board_max[0]+1):
        for j in range(board_max[1]+1):
            dist = calc_tot_dist((j, i), coords, max_dist)
            if dist < max_dist:
                ok += 1
    return ok


def main():
    coords = [(int(val[:val.index(',')]), int(val[val.index(',')+1:])) for val in open(sys.argv[1]).read().split('\n') if val]
    print(calc_max_area(coords))

if __name__ == '__main__':
    main()
