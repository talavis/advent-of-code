import requests

day = 1
part1 = True
part2 = True
testing = True
active = True


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row]
    return data


def calc(data):
    digsum = 0
    for r in data:
        v1 = ""
        v2 = ""
        for c in r:
            if c in "0123456789":
                v1 = c
                break
        for c in r[::-1]:
            if c in "0123456789":
                v2 = c
                break
        digsum += int(v1+v2)
    return digsum


def calc2(data):
    mapper = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    
    digsum = 0
    for r in data:
        v1 = ""
        v2 = ""
        for i in range(len(r)):
            if r[i] in "0123456789":
                v1 = r[i]
                break
            if r[i:i+3] in mapper:
                v1 = mapper[r[i:i+3]]
                break
            if r[i:i+4] in mapper:
                v1 = mapper[r[i:i+4]]
                break
            if r[i:i+5] in mapper:
                v1 = mapper[r[i:i+5]]
                break

        for i in range(len(r)-1, -1, -1):
            if r[i] in "0123456789":
                v2 = r[i]
                break
            if i-2 >= 0 and r[i-2:i+1] in mapper:
                v2 = mapper[r[i-2:i+1]]
                break
            if i-3 >= 0 and r[i-3:i+1] in mapper:
                v2 = mapper[r[i-3:i+1]]
                break
            if i-4 >= 0 and r[i-4:i+1] in mapper:
                v2 = mapper[r[i-4:i+1]]
                break
        digsum += int(v1+v2)
    return digsum


test_data = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

test_data2 = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

if testing:
    test_data = parse(test_data)

    if part1:
        res1 = calc(test_data)
        ans1 = 142
        print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")
    if part2:
        test_data2 = parse(test_data2)
        res2 = calc2(test_data2)
        ans2 = 281
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
