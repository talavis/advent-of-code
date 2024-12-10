import collections

import requests

day = 10
part1 = True
part2 = True
testing = True
active = True

test_data = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

test_data2 = test_data

test_ans1 = 36
test_ans2 = 81


def parse(indata):
    data_rows = indata.split("\n")
    data = [[int(v) for v in row] for row in data_rows if row]
    return data


def calc(data):
    heads = []
    for i, row in enumerate(data):
        for j, v in enumerate(row):
            if v == 0:
                heads.append((i, j))

    def find_access(start):
        dirs = ((1,0), (-1, 0), (0, 1), (0, -1))
        stack = {start}
        tested = {start}
        reachable = {start}
        tops = set()
        while stack:
            work = stack.pop()
            work_val = data[work[0]][work[1]]
            if work_val == 9:
                tops.add(work)
            tested.add(work)
            for d in dirs:
                pos = (work[0] + d[0], work[1] + d[1])
                if (0 <= pos[0] < len(data)) and (0 <= pos[1] < len(data[0])):
                    val = data[pos[0]][pos[1]]
                    if pos not in tested and val - work_val == 1:
                        stack.add(pos)
                        reachable.add(pos)
        return len(tops)
    
    ans = 0
    for pos in heads:
        ans += find_access(pos)
    return ans


def calc2(data):
    heads = []
    for i, row in enumerate(data):
        for j, v in enumerate(row):
            if v == 0:
                heads.append((i, j))

    def find_access(start):
        dirs = ((1,0), (-1, 0), (0, 1), (0, -1))
        stack = [start]
        tops = []
        while stack:
            work = stack.pop()
            work_val = data[work[0]][work[1]]
            if work_val == 9:
                tops.append(work)
            for d in dirs:
                pos = (work[0] + d[0], work[1] + d[1])
                if (0 <= pos[0] < len(data)) and (0 <= pos[1] < len(data[0])):
                    val = data[pos[0]][pos[1]]
                    if val - work_val == 1:
                        stack.append(pos)
        return len(tops)
    
    ans = 0
    for pos in heads:
        ans += find_access(pos)
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
