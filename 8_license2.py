#!/usr/bin/env python3

import sys


def test_find_nodes():
    data = [int(i) for i in '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'.split(' ')]
    assert find_nodes(data) == 66


def find_nodes(data):
    children = [] # nr_children, nr_meta, orig_nr_children, *child_results
    i = 0

    nr_children = data[i]
    nr_meta = data[i+1]
    i += 2
    children.append([nr_children, nr_meta, nr_children])

    while i < len(data):
        # calc metasum
        if children[-1][0] == 0:
            nr_meta = children[-1][1]
            # 0 children
            if children[-1][2] == 0:
                if len(children) == 1:
                    return sum(data[i:i+nr_meta])
                children[-2].append(sum(data[i:i+nr_meta]))
            # checked all children
            else:
                metasum = 0
                for j in range(nr_meta):
                    cnr = data[i+j]-1
                    if len(children[-1])-3 > cnr:
                        metasum += children[-1][cnr+3]
                if len(children) > 1:
                    children[-2].append(metasum)
                elif len(children) == 1:
                    return metasum
            i += nr_meta
            children.pop()
        else:
            children[-1][0] -= 1
            nr_children = data[i]
            nr_meta = data[i+1]
            i += 2
            children.append([nr_children, nr_meta, nr_children])
    return metasum


def main():
    data = [int(i) for i in open(sys.argv[1]).read().strip().split(' ')]
    print(find_nodes(data))


if __name__ == '__main__':
    main()
