#!/usr/bin/env python3

import sys


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

def nr_sec(letter, base_sec=60):
    return base_sec-ord('A')+ord(letter)+1


def test_nr_sec():
    assert nr_sec('C') == 63
    assert nr_sec('C', base_sec=0) == 3


def find_order(info_steps, avail_workers=5, base_sec=60):
    reqs = dict()
    curr_jobs = []
    available = set()
    curr_time = 0
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
    curr_time = nr_sec(result[0], base_sec)
    while len(reqs) > 0:
        if curr_jobs:
            times = [job[1] for job in curr_jobs]
            first = min(times)
            while times.count(first):
                ind = times.index(first)
                result.append(curr_jobs[ind][0])
                done.add(curr_jobs[ind][0])
                del reqs[curr_jobs[ind][0]]
                curr_time = curr_jobs[ind][1]
                curr_jobs.pop(ind)
                times.pop(ind)
                avail_workers += 1

        current = []
        for req in reqs:
            if done.intersection(reqs[req]) == reqs[req]:
                current.append(req)
        current.sort()
        i = 0
        while avail_workers > 0 and i < len(current):
            # job, expected_finish
            if current[i] not in [job[0] for job in curr_jobs]:
                curr_jobs.append((current[i], curr_time + nr_sec(current[i], base_sec)))
                avail_workers -= 1
            i += 1
    return ''.join(result), curr_time


def test_order():
    raw_data = '''Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.'''
    req = parse_input(raw_data)
    assert find_order(req, base_sec=0, avail_workers=2) == ('CABFDE', 15)


def main():
    data = parse_input(open(sys.argv[1]).read())
    res = find_order(data)
    print(res[1])


if __name__ == '__main__':
    main()
