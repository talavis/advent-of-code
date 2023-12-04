import requests

day = 4
part1 = True
part2 = True
testing = True
active = True

test_ans1 = 13
test_ans2 = 30

test_data = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row]
    return data


def calc(data):
    score = 0
    for row in data:
        s = 0
        vals = [int(val) for val in row[row.index(":") + 1 : row.index("|")].strip().split()]
        hits = set(int(hit) for hit in row[row.index("|") + 1 :].strip().split())
        for val in vals:
            if val in hits:
                if s == 0:
                    s += 1
                else:
                    s *= 2
        score += s
    return score


def calc2(data):
    scores = [1] * len(data)
    for i, row in enumerate(data):
        s = 0
        vals = [int(val) for val in row[row.index(":") + 1 : row.index("|")].strip().split()]
        hits = set(int(hit) for hit in row[row.index("|") + 1 :].strip().split())
        for val in vals:
            if val in hits:
                s += 1
        for j in range(s):
            if i + j + 1 < len(scores):
                scores[i + j + 1] += scores[i]
    return sum(scores)


if testing:
    test_data = parse(test_data)

    if part1:
        res1 = calc(test_data)
        ans1 = test_ans1
        print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")
    if part2:
        res2 = calc2(test_data)
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
