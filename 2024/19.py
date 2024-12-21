import functools

import requests

day = 19
part1 = True
part2 = True
testing = True
active = True

test_data = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""

test_data2 = test_data

test_ans1 = 6
test_ans2 = 16


def parse(indata):
    towels, patterns = indata.split("\n\n")
    towels = towels.split(", ")
    patterns = [p for p in patterns.split("\n") if p]
    return towels, patterns


def calc(data):
    towels, patterns = data

    def possible(pattern, selection=None):
        if not pattern:
            return True
        if selection is None:
            selection = set()
            for towel in towels:
                if towel in pattern:
                    selection.add(towel)

        for sel in selection:
            if pattern.startswith(sel):
                if possible(pattern[len(sel) :], selection):
                    return True
        return False

    ans = 0
    for pattern in patterns:
        if possible(pattern):
            ans += 1
    return ans


def calc2(data):
    towels, patterns = data

    @functools.cache
    def possible(pattern, selection=None):
        if not pattern:
            return 1
        if selection is None:
            selection = tuple(towel for towel in towels if towel in pattern)

        combs = 0
        for sel in selection:
            if pattern.startswith(sel):
                combs += possible(pattern[len(sel) :], selection)
        return combs

    ans = 0
    for i, pattern in enumerate(patterns):
        ans += possible(pattern)
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
    with open("cookie.dat") as f:
        cookies = {"session": f.read()}
    try:
        with open(f"{day}.txt") as f:
            raw = f.read()
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
