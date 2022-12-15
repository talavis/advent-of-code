#!/usr/bin/env python3

import sys

SIZE = 1000

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

    for cut in cuts:
        l = int(cut[cut.index('@')+1:cut.index(',')])-1
        t = int(cut[cut.index(',')+1:cut.index(':')])-1
        ls = int(cut[cut.index(':')+1:cut.index('x')])
        ts = int(cut[cut.index('x')+1:])
        shared = 0
        for i in range(t, t+ts):
            for j in range(l, l+ls):
                if square[i][j] > 1:
                    shared += 1
        if not shared:
            return cut


def main():
    cuts = [val for val in open(sys.argv[1]).read().split('\n') if val]
    print(calc_overlap(cuts))

if __name__ == '__main__':
    main()
