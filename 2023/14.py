import requests

day = 14
part1 = True
part2 = True
testing = True
active = True

test_data = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

test_data2 = test_data

test_ans1 = 136
test_ans2 = 64


def parse(indata):
    data_rows = indata.split("\n")
    data = [list(row) for row in data_rows if row]
    return data


def calc(data):
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == "O":
                h = i
                while h > 0 and data[h - 1][j] == ".":
                    h -= 1
                data[i][j] = "."
                data[h][j] = "O"

    score = 0
    for i, row in enumerate(data):
        for c in row:
            if c == "O":
                score += len(data) - i

    return score


def calc2(data):
    def cycle(data):
        for i in range(len(data)):
            for j in range(len(data[0])):
                if data[i][j] == "O":
                    h = i
                    while h > 0 and data[h - 1][j] == ".":
                        h -= 1
                    data[i][j] = "."
                    data[h][j] = "O"
        for i in range(len(data)):
            for j in range(len(data[0])):
                if data[i][j] == "O":
                    h = j
                    while h > 0 and data[i][h - 1] == ".":
                        h -= 1
                    data[i][j] = "."
                    data[i][h] = "O"
        for i in range(len(data) - 1, -1, -1):
            for j in range(len(data[0])):
                if data[i][j] == "O":
                    h = i
                    while h < len(data) - 1 and data[h + 1][j] == ".":
                        h += 1
                    data[i][j] = "."
                    data[h][j] = "O"
        for i in range(len(data)):
            for j in range(len(data[0]) - 1, -1, -1):
                if data[i][j] == "O":
                    h = j
                    while h < len(data[0]) - 1 and data[i][h + 1] == ".":
                        h += 1
                    data[i][j] = "."
                    data[i][h] = "O"

    res = []
    start = 0
    end = 1000000000
    for i in range(end):
        cycle(data)
        score = 0
        for j, row in enumerate(data):
            for c in row:
                if c == "O":
                    score += len(data) - j

        # find cycle
        if score in res and i > 10:  # 10: arbitrary number to avoid issue with test data
            start = res.index(score)
            r_cycle = res[start:]
            return r_cycle[(end - i - 1) % len(r_cycle)]
        res.append(score)

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
        raw = requests.get(f"https://adventofcode.com/2023/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    if part1:
        data = parse(raw)
        print(f"Part 1: {calc(data)}")
    if part2:
        data = parse(raw)
        print(f"Part 2: {calc2(data)}")
