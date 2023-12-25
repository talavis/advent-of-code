import requests

day = 2
part1 = True
part2 = True
testing = True
active = True

test_data = """
forward 5
down 5
forward 8
up 3
down 8
forward 2
"""

test_data2 = test_data

test_ans1 = 150
test_ans2 = 900


def parse(indata):
    data_rows = indata.split("\n")
    data = []
    for row in data_rows:
        if row:
            cols = row.split()
            data.append((cols[0], int(cols[1])))
    return data


def calc(data):
    y = 0
    x = 0
    for row in data:
        if row[0] == "forward":
            x += row[1]
        elif row[0] == "down":
            y += row[1]
        elif row[0] == "up":
            y -= row[1]

    return x * y


def calc2(data):
    aim = 0
    y = 0
    x = 0
    for row in data:
        if row[0] == "forward":
            x += row[1]
            y += aim * row[1]
        elif row[0] == "down":
            aim += row[1]
        elif row[0] == "up":
            aim -= row[1]
    return x * y


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
