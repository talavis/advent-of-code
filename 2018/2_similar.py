#!/usr/bin/env python3

from collections import Counter
import sys


def similar(ids):
    for i in range(len(ids)):
        for j in range(i+1, len(ids)):
            dist = 0
            k = 0
            pos = 0
            while k < len(ids[i]) and dist <= 1:
                if ids[i][k] != ids[j][k]:
                    dist += 1
                    pos = k
                k += 1
            if dist == 1:
                return ids[i][:pos] + ids[i][pos+1:]


def test_similar():
    ids = ('abcde', 'fghij', 'klmno', 'pqrst', 'fguij', 'axcye', 'wvxyz')
    assert similar(ids) == 'fgij'


def main():
    ids = tuple(val for val in open(sys.argv[1]).read().split('\n') if val)
    print(similar(ids))
    

if __name__ == '__main__':
    main()
