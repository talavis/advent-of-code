#!/usr/bin/env python3

import sys

SIZE = 1000

def test_calc():
    cuts = ['#1 @ 1,3: 4x4',
            '#2 @ 3,1: 4x4',
            '#3 @ 5,5: 2x2']
    assert calc_overlap(cuts, size=8) == 4

def calc_overlap(cuts, size = 1000):
    square = [size*[0] for i in range(size)]
    for cut in cuts:
        l = int(cut[cut.index('@')+1:cut.index(',')])-1
        t = int(cut[cut.index(',')+1:cut.index(':')])-1
        ls = int(cut[cut.index(':')+1:cut.index('x')])
        ts = int(cut[cut.index('x')+1:])
        for i in range(t, t+ts):
            for j in range(l, l+ls):
                square[i][j] += 1
    shared = 0
    for row in square:
        for col in row:
            if col > 1:
                shared += 1
    return shared


def main():
    cuts = [val for val in open(sys.argv[1]).read().split('\n') if val]
    print(calc_overlap(cuts))

if __name__ == '__main__':
    main()
