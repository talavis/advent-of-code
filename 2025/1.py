import requests

day = 1
part1 = True
part2 = True
testing = True
active = True

test_data = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""

test_data2 = test_data

test_ans1 = 3
test_ans2 = 6


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row]
    return data


def calc(data):
    ans = 0
    dial = 50
    for r in data:
        if r[0] == "L":
            s = -1
        else:
            s = 1
        dial = (dial + s * int(r[1:]) ) % 100
        if dial == 0:
            ans += 1    
    return ans


def calc2(data):
    ans = 0
    dial = 50
    for r in data:
        if r[0] == "L":
            s = -1
        else:
            s = 1
        step = int(r[1:])
        ans += step // 100
        step = step % 100
        dial_old = dial
        dial = dial + s * step
        if dial % 100 != dial and dial_old:
            ans += 1
        if dial == 0:
            ans += 1
        dial %= 100
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
        raw = requests.get(f"https://adventofcode.com/2025/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    if part1:
        data = parse(raw)
        print(f"Part 1: {calc(data)}")
    if part2:
        data = parse(raw)
        print(f"Part 2: {calc2(data)}")
