import requests

day = 9
part1 = True
part2 = True
testing = True
active = True

test_data = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

test_ans1 = 114
test_ans2 = 2


def parse(indata):
    data_rows = indata.split("\n")
    data = [[int(e) for e in row.split()] for row in data_rows if row]
    return data


def calc(data):
    def next_val(sequence):
        vals = set(sequence)
        if len(vals) == 1 and vals.pop() == 0:
            return 0
        else:
            diffs = []
            for i, s in enumerate(sequence):
                if i == 0:
                    continue
                diffs.append(s - sequence[i - 1])
            base = next_val(diffs)
            return base + sequence[-1]

    score = 0
    for row in data:
        res = next_val(row)
        score += res

    return score


def calc2(data):
    def next_val(sequence):
        vals = set(sequence)
        if len(vals) == 1 and vals.pop() == 0:
            return 0
        else:
            diffs = []
            for i, s in enumerate(sequence):
                if i == 0:
                    continue
                diffs.append(s - sequence[i - 1])
            base = next_val(diffs)
            return sequence[0] - base

    score = 0
    for row in data:
        res = next_val(row)
        score += res

    return score


if testing:
    test_data_p = parse(test_data)

    if part1:
        res1 = calc(test_data_p)
        ans1 = test_ans1
        print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")
    if part2:
        res2 = calc2(test_data_p)
        ans2 = test_ans2
        print(f"Test part 2: {res2} ({ans2}){'   !!!' if res2 != ans2 else ''}")

if active:
    cookies = {"session": open("cookie.dat").read()}
    try:
        raw = open(f"{day}.txt").read()
    except FileNotFoundError:
        raw = requests.get(f"https://adventofcode.com/2023/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    data = parse(raw)
    if part1:
        print(f"Part 1: {calc(data)}")
    if part2:
        print(f"Part 2: {calc2(data)}")
