import requests

day = 3
part1 = True
part2 = True
testing = True
active = True

test_ans1 = 4361
test_ans2 = 467835

test_data = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row]
    return data


def calc(data):
    def find_symbol(r, x1, x2):
        start_r = r-1
        if r == 0:
            start_r = 0
        end_r = r+1
        if end_r >= len(data):
            end_r = r

        start_x = x1-1
        if x1 == 0:
            start_x = 0
        end_x = x2+1
        if end_x >= len(data[r]):
            end_x = x2

        for i in range(start_r, end_r+1):
            for j in range(start_x, end_x+1):
                if data[i][j] not in "0123456789.":
                    return True
        return False

    score = 0
    numbers = []

    for r in range(len(data)):
        num = [-1, -1]
        for c in range(len(data[r])):
            if data[r][c] in "0123456789":
                if num[0] == -1:
                    num[0] = c
                    num[1] = c
                else:
                    num[1] = c
            elif num[0] != -1:
                numbers.append((r, num[0], num[1]))
                if find_symbol(r, num[0], num[1]):
                    score += int(data[r][num[0]:num[1]+1])
                num = [-1, -1]
        if num[0] != -1:
            numbers.append((r, num[0], num[1]))
            if find_symbol(r, num[0], num[1]):
                score += int(data[r][num[0]:num[1]+1])
            num = [-1, -1]
    return score


def calc2(data):
    def find_gear(r, x1, x2, gears):
        start_r = r-1
        if r == 0:
            start_r = 0
        end_r = r+1
        if end_r >= len(data):
            end_r = r

        start_x = x1-1
        if x1 == 0:
            start_x = 0
        end_x = x2+1
        if end_x >= len(data[r]):
            end_x = x2

        for i in range(start_r, end_r+1):
            for j in range(start_x, end_x+1):
                if data[i][j] == "*":
                    gears[(i,j)].append(int(data[r][x1:x2+1]))

    score = 0
    numbers = []
    gears = {} # {(r,x): [numbers]}

    for r in range(len(data)):
        num = [-1, -1]
        for c in range(len(data[r])):
            if data[r][c] == "*":
                gears[(r,c)] = []
            if data[r][c] in "0123456789":
                if num[0] == -1:
                    num[0] = c
                    num[1] = c
                else:
                    num[1] = c
            elif num[0] != -1:
                numbers.append((r, num[0], num[1]))
                num = [-1, -1]
        if num[0] != -1:
            numbers.append((r, num[0], num[1]))
            num = [-1, -1]

    for num in numbers:
        find_gear(*num, gears)
    for gear in gears:
        if len(gears[gear]) == 2:
            score += gears[gear][0] * gears[gear][1] 

    return score


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
