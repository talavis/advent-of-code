import requests

day = 1
testing = True
active = False


def parse(indata):
    data_rows = raw.split("\n")
    data = [row for row in data_rows if row]
    return data


def calc(data):
    score = 0
    return score


def calc2(data):
    score = 0
    return score


test_data = """
"""

test_data = parse(testdata)

if testing:
    res1 = calc(test_data)
    res2 = calc2(test_data)
    ans1 = -1
    ans2 = -1
    print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")
    print(f"Test part 2: {res2} ({ans2}){'   !!!' if res2 != ans2 else ''}")

if active:
    cookies = {"session": open("cookie.dat").read()}
    try:
        raw = open(f"{day}.txt").read()
    except FileNotFoundError:
        raw = requests.get(f"https://adventofcode.com/2022/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    data = parse(raw)
    print(f"Part 1: {calc(data)}")
    print(f"Part 2: {calc2(data)}")
