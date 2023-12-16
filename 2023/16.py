import requests

day = 16
part1 = True
part2 = True
testing = True
active = True

test_data = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""

test_data2 = test_data

test_ans1 = 46
test_ans2 = 51


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row]
    return data


def calc(data):
    direct = ((-1, 0), (1, 0), (0, -1), (0, 1))  # udlr

    def beam(p, d, past):
        while 0 <= p[0] < len(data) and 0 <= p[1] < len(data[0]) and (p[0], p[1], d) not in past:
            past.add((p[0], p[1], d))
            if data[p[0]][p[1]] == "-":
                if d not in (2, 3):  # lr
                    d = 2
                    beam(list(p), 3, past)
            elif data[p[0]][p[1]] == "|":
                if d not in (0, 1):  # ud
                    d = 0
                    beam(list(p), 1, past)
            elif data[p[0]][p[1]] == "/":
                if d == 0:  # u
                    d = 3  # r
                elif d == 1:  # d
                    d = 2  # l
                elif d == 2:  # l
                    d = 1  # d
                elif d == 3:  # r
                    d = 0  # u
            elif data[p[0]][p[1]] == "\\":
                if d == 0:  # u
                    d = 2  # l
                elif d == 1:  # d
                    d = 3  # r
                elif d == 2:  # l
                    d = 0  # u
                elif d == 3:  # r
                    d = 1  # d
            p[0] = p[0] + direct[d][0]
            p[1] = p[1] + direct[d][1]

    past = set()
    res = [[0] * len(data[0]) for _ in range(len(data))]
    beam([0, 0], 3, past)
    past.add((0, 0, 3))
    score = len(set((p[0], p[1]) for p in past))
    return score


def calc2(data):
    direct = ((-1, 0), (1, 0), (0, -1), (0, 1))  # udlr

    def beam(p, d, past):
        while 0 <= p[0] < len(data) and 0 <= p[1] < len(data[0]) and (p[0], p[1], d) not in past:
            past.add((p[0], p[1], d))
            if data[p[0]][p[1]] == "-":
                if d not in (2, 3):  # lr
                    d = 2
                    beam(list(p), 3, past)
            elif data[p[0]][p[1]] == "|":
                if d not in (0, 1):  # ud
                    d = 0
                    beam(list(p), 1, past)
            elif data[p[0]][p[1]] == "/":
                if d == 0:  # u
                    d = 3  # r
                elif d == 1:  # d
                    d = 2  # l
                elif d == 2:  # l
                    d = 1  # d
                elif d == 3:  # r
                    d = 0  # u
            elif data[p[0]][p[1]] == "\\":
                if d == 0:  # u
                    d = 2  # l
                elif d == 1:  # d
                    d = 3  # r
                elif d == 2:  # l
                    d = 0  # u
                elif d == 3:  # r
                    d = 1  # d
            p[0] = p[0] + direct[d][0]
            p[1] = p[1] + direct[d][1]

    best = 0
    for i in range(len(data)):
        past = set()
        beam([i, 0], 3, past)
        past.add((i, 0, 3))
        score = len(set((p[0], p[1]) for p in past))
        if score > best:
            best = score
        past = set()
        beam([i, len(data[0]) - 1], 2, past)
        past.add((i, len(data[0]) - 1, 2))
        score = len(set((p[0], p[1]) for p in past))
        if score > best:
            best = score
    for i in range(len(data[0])):
        past = set()
        beam([0, i], 1, past)
        past.add((0, i, 1))
        score = len(set((p[0], p[1]) for p in past))
        if score > best:
            best = score
        past = set()
        beam([len(data) - 1, i], 0, past)
        past.add((len(data) - 1, i, 0))
        score = len(set((p[0], p[1]) for p in past))
        if score > best:
            best = score

    return best


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
        raw = requests.get(f"https://adventofcode.com/2023/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    if part1:
        data = parse(raw)
        print(f"Part 1: {calc(data)}")
    if part2:
        data = parse(raw)
        print(f"Part 2: {calc2(data)}")
