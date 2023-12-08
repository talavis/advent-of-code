import requests

day = 8
part1 = True
part2 = True
testing = True
active = True

test_data = """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

test_data2 = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

test_ans1 = 2
test_ans2 = 6


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row]
    paths = {"directions": data[0]}
    for path in data[1:]:
        parts = path.split()
        paths[parts[0]] = (parts[2][1:-1], parts[3][:-1])
    return paths


def calc(data):
    def direction():
        i = 0
        while True:
            d = data["directions"][i]
            if d == "R":
                yield 1
            if d == "L":
                yield 0
            i += 1
            if i >= len(data["directions"]):
                i = 0

    pos = "AAA"
    s = 0
    d = direction()
    while pos != "ZZZ":
        s += 1
        pos = data[pos][next(d)]

    return s


def calc2(data):
    def direction():
        i = 0
        while True:
            d = data["directions"][i]
            if d == "R":
                yield 1
            if d == "L":
                yield 0
            i += 1
            if i >= len(data["directions"]):
                i = 0

    def find_divisors(value):
        i = 2
        divs = []
        while value >= i:
            if value % i == 0:
                divs.append(i)
                value //= i
            else:
                i += 1
        return divs

    def gcd(values):
        divs = []
        for v in values:
            divs.append(find_divisors(v))
        res = []
        for d in divs:
            for v in d:
                while res.count(v) < d.count(v):
                    res.append(v)
        return res

    pos = [p for p in data.keys() if p.endswith("A")]
    s = 0
    dg = direction()

    diffs = [-1] * len(pos)
    while True:
        s += 1
        d = next(dg)
        for i, p in enumerate(pos):
            pos[i] = data[p][d]
            # doubtful this always works, but for my data the cycle was always the same
            if pos[i].endswith("Z") and diffs[i] == -1:
                diffs[i] = s
        if -1 not in diffs:
            break
    d = gcd(diffs)
    score = 1
    for v in d:
        score *= v
    return score


if testing:
    test_data_p = parse(test_data)
    test_data_p2 = parse(test_data2)
    if part1:
        res1 = calc(test_data_p)
        ans1 = test_ans1
        print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")
    if part2:
        res2 = calc2(test_data_p2)
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
