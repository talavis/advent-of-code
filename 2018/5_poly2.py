#!/usr/bin/env python3

import string
import sys

CONVERTER = dict(zip(string.ascii_lowercase + string.ascii_uppercase,
                     string.ascii_uppercase + string.ascii_lowercase))

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
    i = 0
    while i < len(seq)-1:
        if seq[i] == CONVERTER[seq[i+1]]:
            seq = seq[:i]+seq[i+2:]
            if i > 0:
                i -= 1
        else:
            i += 1
    return seq 
       

def main():
    seq = open(sys.argv[1]).read().strip()
    print(find_shortest_rm(seq))


if __name__ == '__main__':
    main()
