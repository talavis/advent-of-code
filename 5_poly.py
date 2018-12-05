#!/usr/bin/env python3

import string
import sys

def test_calc():
    seq = 'dabAcCaCBAcCcaDA'
    assert calc_poly(seq) == 'dabCBAcaDA'

    
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
    print(len(calc_poly(seq)))


if __name__ == '__main__':
    main()
