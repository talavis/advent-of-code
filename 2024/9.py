import collections

import requests

day = 9
part1 = True
part2 = True
testing = True
active = True

test_data = """
2333133121414131402
"""

test_data2 = test_data

test_ans1 = 1928
test_ans2 = 2858


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row][0]
    return data


def calc(data):
    storage = []
    b = 0
    for i, d in enumerate(data):
        v = int(d)
        if i % 2 == 0:
            storage.extend([b] * v)
            b += 1
        else:
            storage.extend([None] * v)
    i = 0
    while i < len(storage) - 1:
        if storage[i] is None:
            d = storage.pop()
            while d is None and len(storage) + 1 > i:
                d = storage.pop()
            storage[i] = d
            i += 1
        else:
            i += 1

    ans = 0
    for i in range(len(storage)):
        if storage[i] is not None:
            ans += i * storage[i]

    return ans


def calc2(data):
    storage = []
    blocks = {}
    b = 0
    for i, d in enumerate(data):
        v = int(d)
        if i % 2 == 0:
            storage.extend([b] * v)
            blocks[b] = v
            b += 1
        else:
            storage.extend([None] * v)

    i = 0
    b = max(blocks.keys())
    while b > 0:
        print(b)
        l = blocks[b]
        i = 0
        sl = 0
        e = len(storage) - 1
        start = 0
        while sl < l and storage[i] != b:
            if storage[i] is None:
                if sl == 0:
                    start = i
                sl += 1
            else:
                sl = 0
            i += 1
        if sl == l:
            started = False
            while storage[e] in (b, None):
                storage[e] = None
                e -= 1
        b -= 1

    ans = 0
    for i in range(len(storage)):
        if storage[i] is not None:
            ans += i * storage[i]

    return ans


if testing:
    if part1:
        test_data_p = parse(test_data)
        res1 = calc(test_data_p)
        ans1 = test_ans1
        print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")

    if part2:
        test_data_p2 = parse(test_data2)
        res2 = calc2(test_data_p2)
        ans2 = test_ans2
        print(f"Test part 2: {res2} ({ans2}){'   !!!' if res2 != ans2 else ''}")

if active:
    cookies = {"session": open("cookie.dat").read()}
    try:
        raw = open(f"{day}.txt").read()
    except FileNotFoundError:
        raw = requests.get(f"https://adventofcode.com/2024/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    if part1:
        data = parse(raw)
        print(f"Part 1: {calc(data)}")
    if part2:
        data = parse(raw)
        print(f"Part 2: {calc2(data)}")
