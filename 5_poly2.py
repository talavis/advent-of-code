#!/usr/bin/env python3

import string
import sys

def test_short():
    seq = 'dabAcCaCBAcCcaDA'
    assert find_shortest_rm(seq) == 4


def test_calc():
    seq = 'dabAcCaCBAcCcaDA'
    assert calc_poly(seq) == 'dabCBAcaDA'

    
def find_shortest_rm(seq):
    shortest = len(seq)
    for c in string.ascii_lowercase:
        new_seq = seq.replace(c, '')
        new_seq = new_seq.replace(c.upper(), '')
        poly = calc_poly(new_seq)
        if len(poly) < shortest:
            shortest = len(poly)
    return shortest
        

def calc_poly(seq):
    old_len = 0
    while old_len != len(seq):
        old_len = len(seq)
        for c in string.ascii_lowercase:
            seq = seq.replace(c + c.upper(), '')
            seq = seq.replace(c.upper() + c, '')
    return seq 
       

def main():
    seq = open(sys.argv[1]).read().strip()
    print(find_shortest_rm(seq))


if __name__ == '__main__':
    main()
