import collections

import requests

day = 7
part1 = True
part2 = True
testing = True
active = True

test_data = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

test_data2 = test_data

test_ans1 = 3749
test_ans2 = 11387


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row]
    for i in range(len(data)):
        cols = data[i].split()
        data[i] = (int(cols[0][:-1]), [int(v) for v in cols[1:]])
    return data


def calc(data):
    def step(start, goal, remaining):
        if not remaining:
            if start == goal:
                return goal
            else:
                return 0
        res = step(start + remaining[0], goal, remaining[1:])
        if res > 0:
            return res
        return step(start * remaining[0], goal, remaining[1:])
    
    ans = 0
    for row in data:
        ans += step(0, row[0], row[1])

    return ans


def calc2(data):
    def step(start, goal, remaining):
        if not remaining:
            if start == goal:
                return goal
            else:
                return 0
        res = step(start + remaining[0], goal, remaining[1:])
        if res > 0:
            return res
        res = step(start * remaining[0], goal, remaining[1:])
        if res > 0:
            return res
        return step(int(str(start) + str(remaining[0])), goal, remaining[1:])
    
    ans = 0
    for row in data:
        ans += step(0, row[0], row[1])

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
