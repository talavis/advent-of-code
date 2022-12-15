#!/usr/bin/env python3

import sys


def test_find_nodes():
    data = [int(i) for i in '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'.split(' ')]
    assert find_nodes(data) == 138


def find_nodes(data):
    metasum = 0
    children = [] # nr_children, nr_meta
    i = 0

    nr_children = data[i]
    nr_meta = data[i+1]
    i += 2
    children.append([nr_children, nr_meta])

    while i < len(data):
        if children[-1][0] == 0:
            nr_meta = children[-1][1]
            metasum += sum(data[i:i+nr_meta])
            i += nr_meta
            children.pop()
        else:
            children[-1][0] -= 1
            nr_children = data[i]
            nr_meta = data[i+1]
            i += 2
            children.append([nr_children, nr_meta])
    return metasum


def main():
    data = [int(i) for i in open(sys.argv[1]).read().strip().split(' ')]
    print(find_nodes(data))


if __name__ == '__main__':
    main()
