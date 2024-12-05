import collections

import requests

day = 4
part1 = True
part2 = True
testing = True
active = True

test_data = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

test_data2 = test_data

test_ans1 = 18
test_ans2 = 9


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row]
    return data


# Assumes all letters are unique
def calc(data, word="XMAS"):
    directions = []
    for a in (-1, 0, 1):
        for b in (-1, 0, 1):
            if a != 0 or b != 0:
                directions.append((a, b))

    def find_word(i, j):
        if data[i][j] != word[0]:
            return 0
        count = 0
        for d in directions:
            count += test_match(i, j, d)
        return count
    
    def test_match(i, j, direction):
        for s in range(1, len(word)):
            i += direction[0]
            j += direction[1]
            if not (0 <= i < len(data)) or not (0 <= j < len(data[0])):
                return 0
            if data[i][j] != word[s]:
                return 0
        return 1
          
    count = 0
    for i in range(len(data)):
        for j in range(len(data[0])):
            count += find_word(i, j)
    return count


def calc2(data):
    count = 0
    for i in range(1, len(data)-1):
        for j in range(1, len(data[0])-1):
            if data[i][j] == "A":
                if data[i-1][j-1]+data[i+1][j+1] in ("MS", "SM") and data[i+1][j-1]+data[i-1][j+1] in ("MS", "SM"):
                    count += 1
    return count


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
        raw = requests.get(f"https://adventofcode.com/2024/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    if part1:
        data = parse(raw)
        print(f"Part 1: {calc(data)}")
    if part2:
        data = parse(raw)
        print(f"Part 2: {calc2(data)}")


# M M  M S
#  A    A
# S S  S M
