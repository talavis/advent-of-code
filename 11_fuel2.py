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
    assert find_cells(18) == (90, 269, 16, 113)
    assert find_cells(42) == (232, 251, 12, 119)


def find_cells(serial):
    fuel_array = [[0]*300 for i in range(300)]
    for i in range(len(fuel_array)):
        for j in range(len(fuel_array[0])):
            fuel_array[i][j] = get_level((i+1, j+1), serial)

    best = (-1, -1, 0, float('-inf'))
    for size in range(1, 30):
        print(size)
        for i in range(len(fuel_array)-size+1):
            for j in range(len(fuel_array[0])-size+1):
                curr_sum = 0
                for k in range(size):
                    curr_sum += sum(fuel_array[i+k][j:j+size])
#                print(i+1,j+1,curr_sum)
                if curr_sum > best[3]:
                    best = (i+1, j+1, size, curr_sum)
                    print(best)
    return best


def main():
    serial = 9110
    res = find_cells(serial)
    print(f'{res[0]},{res[1]},{res[2]}')
    

if __name__ == '__main__':
    main()
