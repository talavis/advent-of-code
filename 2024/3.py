import collections
import re

import requests


day = 3
part1 = True
part2 = True
testing = True
active = True

test_data = """
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""

test_data2 = """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""

test_ans1 = 161
test_ans2 = 48


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row]
    return data


def calc(data):
    ans = 0
    for d in data:
        hits = re.findall(r"mul\(([1-9][0-9]*),([1-9][0-9]*)\)", d)
        for hit in hits:
            ans += int(hit[0]) * int(hit[1])
    return ans


def calc2(data):
    ans = 0
    skip = False
    for d in data:
        hits = re.findall(r"(mul\(([1-9][0-9]*),([1-9][0-9]*)\))|(don\'t\(\)|(do\(\)))", d)
        for hit in hits:
            if "do()" in hit:
                skip = False
            elif "don't()" in hit:
                skip = True
            elif not skip:
                ans += int(hit[1]) * int(hit[2])
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
