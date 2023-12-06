import requests

day = 6
part1 = True
part2 = True
testing = True
active = True

test_ans1 = 288
test_ans2 = 71503

test_data = """
Time:      7  15   30
Distance:  9  40  200
"""


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row]
    return data


def calc(data):
    score = 1
    time = [int(val) for val in data[0][data[0].index(":") + 1 :].split()]
    dist = [int(val) for val in data[1][data[1].index(":") + 1 :].split()]
    data = list(zip(time, dist))
    for d in data:
        wins = 0
        for t in range(d[0]):
            if t * (d[0] - t) > d[1]:
                wins += 1
        score *= wins
    return score


def calc2(data):
    time = int("".join(data[0][data[0].index(":") + 1 :].strip().split()))
    dist = int("".join(data[1][data[1].index(":") + 1 :].strip().split()))
    score = 0
    # didn't expect the numbers to be small enough for this to be ok :O
    for t in range(time):
        if t * (time - t) > dist:
            score += 1
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
