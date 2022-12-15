import requests

day = 6


def calc(data):
    for i in range(4, len(data)):
        if len(set(data[i - 4 : i])) == 4:
            return i
    return 0


def calc2(data):
    for i in range(14, len(data)):
        if len(set(data[i - 14 : i])) == 14:
            return i
    return 0


cookies = {"session": open("cookie.dat").read()}
req = requests.get(f"https://adventofcode.com/2022/day/{day}/input", cookies=cookies)
data = req.text

print(f"Part 1: {calc(data)}")
print(f"Part 2: {calc2(data)}")
