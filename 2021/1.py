import requests

day = 1
part1 = True
part2 = True
testing = True
active = True

test_data = """
199
200
208
210
200
207
240
269
260
263
"""

test_data2 = test_data

test_ans1 = 7
test_ans2 = 5


def parse(indata):
    data_rows = indata.split("\n")
    data = [int(row) for row in data_rows if row]
    return data


def calc(data):
    score = 0
    last = float("inf")
    for d in data:
        if d > last:
            score += 1
        last = d
    return score


def calc2(data):
    score = 0
    last = sum(data[:3])
    for i in range(3, len(data)):
        new_sum = sum(data[i - 2 : i + 1])
        if last < new_sum:
            score += 1
        last = new_sum
    return score


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
        raw = requests.get(f"https://adventofcode.com/2021/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    if part1:
        data = parse(raw)
        print(f"Part 1: {calc(data)}")
    if part2:
        data = parse(raw)
        print(f"Part 2: {calc2(data)}")
