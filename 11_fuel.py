#!/usr/bin/env python3

import sys

def test_get_level():
    assert get_level([3,5], 8) == 4
    assert get_level([122,79], 57) == -5
    assert get_level([217,196], 39) == 0
    assert get_level([101,153], 71) == 4


def get_level(coord, serial):
    rack = coord[0]+10
    level = rack*coord[1]
    level += serial
    level *= rack
    hundreds = (level%1000)//100
    return hundreds-5


def test_find_cells():
    assert find_cells(18) == (33, 45, 29)
    assert find_cells(42) == (21, 61, 30)


def find_cells(serial):
    fuel_array = [[0]*300 for i in range(300)]
    for i in range(len(fuel_array)):
        for j in range(len(fuel_array[0])):
            fuel_array[i][j] = get_level((i+1, j+1), serial)
    best = (-1, -1, float('-inf'))
    for i in range(len(fuel_array)-2):
        for j in range(len(fuel_array[0])-2):
            current = fuel_array[i][j:j+3]
            current += fuel_array[i+1][j:j+3]
            current += fuel_array[i+2][j:j+3]
            if sum(current) > best[2]:
                best = (i+1, j+1, sum(current))
    return best


def main():
    serial = 9110
    res = find_cells(serial)
    print(f'{res[0]}, {res[1]}')
    

if __name__ == '__main__':
    main()
