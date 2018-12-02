#!/usr/bin/env python3

from collections import Counter
import sys

def checksum(ids):
    threes = 0
    twos = 0
    for val in ids:
        counter = Counter(val)
        if 2 in counter.values():
            twos += 1
        if 3 in counter.values():
            threes += 1
    return threes*twos
                

def test_checksum():
    ids = ('abcdef', 'bababc', 'abbcde',
           'abcccd', 'aabcdd', 'abcdee',
           'ababab')
    assert checksum(ids) == 12


def main():
    ids = (val for val in open(sys.argv[1]).read().split('\n') if val)
    print(checksum(ids))
    

if __name__ == '__main__':
    main()
