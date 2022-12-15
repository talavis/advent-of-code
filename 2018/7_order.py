#!/usr/bin/env python3

import sys

def test_order():
    raw_data = '''Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.'''
    req = parse_input(raw_data)
    assert find_order(req) == 'CABDFE'


def parse_input(rawdata):
    steps = []
    for line in rawdata.split('\n'):
        if line:
            steps.append((line[5], line[36]))
    return steps


def test_parse_input():
    rawdata = '''Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.'''
    assert parse_input(rawdata) == [('C', 'A'),
                                    ('C', 'F'),
                                    ('A', 'B'),
                                    ('A', 'D'),
                                    ('B', 'E'),
                                    ('D', 'E'),
                                    ('F', 'E')]


def find_order(info_steps):
    reqs = dict()
    available = set()
    for step in info_steps:
        if step[1] not in reqs:
            reqs[step[1]] = {step[0]}
        else:
            reqs[step[1]].add(step[0])
        available.add(step[0])
        available.add(step[1])
    result = []
    for avail in available:
        if avail not in reqs:
            result = [avail]
            break
    done = set(result)
    while len(reqs) > 0:
        current = []

        for req in reqs:
            if done.intersection(reqs[req]) == reqs[req]:
                current.append(req)
        current.sort()
        result.append(current[0])
        done.add(current[0])
        del reqs[current[0]]
    return ''.join(result)



def main():
    data = parse_input(open(sys.argv[1]).read())
    print(find_order(data))

if __name__ == '__main__':
    main()
