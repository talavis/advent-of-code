import requests

day = 2
part1 = True
part2 = True
testing = True
active = True

test_ans1 = 8
test_ans2 = 2286


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row]
    rgb_words = ["red", "green", "blue"]
    for i in range(len(data)):
        dat = data[i]
        dat = dat[dat.index(":") + 1 :]
        fac = dat.split(";")
        rgb = [0, 0, 0]
        for f in fac:
            parts = f.split(",")
            for p in parts:
                dc = p.strip().split(" ")
                rgb[rgb_words.index(dc[1])] = max(int(dc[0]), rgb[rgb_words.index(dc[1])])
        data[i] = rgb

    return data


def calc(data):
    score = 0
    for i, rgb in enumerate(data):
        if rgb[0] <= 12 and rgb[1] <= 13 and rgb[2] <= 14:
            score += i + 1
    return score


def calc2(data):
    score = 0
    for rgb in data:
        score += rgb[0] * rgb[1] * rgb[2]
    return score


test_data = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

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
