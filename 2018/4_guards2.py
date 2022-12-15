#!/usr/bin/env python3

import sys

def test_minute():
    assert find_minute('[1518-05-29 00:10] falls asleep') == 10
    assert find_minute('[1518-05-15 23:53] Guard #2749 begins shift') == 0

    
def find_minute(entry):
    timestamp = entry[12:17]
    if timestamp[:2] == '23':
        return 0
    else:
        return int(timestamp[3:])

    
def find_sleepy(data):
    guard_sleep = dict()
    guard_id = -1
    sleep_start = -1
    for dat in data:
        if '#' in dat:
            start = dat.index('#')
            guard_id = int(dat[start+1:dat.index(' ', start)])
            if guard_id not in guard_sleep:
                guard_sleep[guard_id] = [0 for i in range(60)]
        if 'falls asleep' in dat:
            sleep_start = find_minute(dat)
        if 'wakes up' in dat:
            for i in range(sleep_start, find_minute(dat)):
                guard_sleep[guard_id][i] += 1
    best_min = -1
    best_guard = -1
    for guard in guard_sleep:
        tmp = max(guard_sleep[guard])
        if tmp > best_min:
            best_min = tmp
            best_guard = guard
    return(best_guard, guard_sleep[best_guard].index(best_min))


def test_sleepy():
    dat = '''[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up'''.split('\n')

    assert find_sleepy(dat) == (99, 45)


def main():
    data = sorted(tuple(val for val in open(sys.argv[1]).read().split('\n') if val))
    result = find_sleepy(data)
    print(result[0]*result[1])

if __name__ == '__main__':
    main()
