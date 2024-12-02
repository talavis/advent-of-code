import collections

import requests

day = 2
part1 = True
part2 = True
testing = True
active = True

test_data = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

test_data2 = test_data

test_ans1 = 2
test_ans2 = 4


def parse(indata):
    data_rows = indata.split("\n")
    data = [[int(c) for c in row.split()] for row in data_rows if row]
    return data


def calc(data):
    def eval(report):
        if report[0] == report[1]:
            return False
        inc = report[0] < report[1]
        current = report[0]
        safe = True
        for i in range(1, len(report)):
            change = current - report[i]
            if abs(change) > 3 or abs(change) < 1:
                safe = False
                break
            if (current < report[i]) != inc or current == report[i]:
                safe = False
                break
            current = report[i]
        if safe:
            return True
        return False

    total = 0
    for report in data:
        total += eval(report)
    return total


def calc2(data):
    def eval(report):
        if report[0] == report[1]:
            return False
        inc = report[0] < report[1]
        current = report[0]
        safe = True
        for i in range(1, len(report)):
            change = current - report[i]
            if abs(change) > 3 or abs(change) < 1:
                safe = False
                break
            if (current < report[i]) != inc or current == report[i]:
                safe = False
                break
            current = report[i]
        if safe:
            return True
        return False

    total = 0
    for report in data:
        res = eval(report)
        if res:
            total += 1
        else:
            for i in range(len(report)):
                res = eval(report[:i] + report[i+1:])
                if res:
                    total += 1
                    break
    return total



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
