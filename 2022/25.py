import requests

day = 25
testing = True
active = True


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row]
    return data


def val_to_snafu(total):
    out = ""
    while total > 0:
        rem = total % 5
        if rem == 3:
            out = "=" + out
            total -= -2
        elif rem == 4:
            out = "-" + out
            total -= -1
        else:
            out = str(rem) + out
            total -= rem
        total //= 5
    return out


def calc(data):
    total = 0
    for row in data:
        multi = len(row) - 1
        val = 0
        for i, c in enumerate(row):
            if c == "=":
                val += 5 ** (multi - i) * -2
            elif c == "-":
                val += 5 ** (multi - i) * -1
            else:
                val += 5 ** (multi - i) * int(c)
        total += val
    return val_to_snafu(total)


test_data = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""

if testing:
    test_data = parse(test_data)

    res1 = calc(test_data)
    ans1 = "2=-1=0"
    print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")

if active:
    cookies = {"session": open("cookie.dat").read()}
    try:
        raw = open(f"{day}.txt").read()
    except FileNotFoundError:
        raw = requests.get(f"https://adventofcode.com/2022/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    data = parse(raw)
    print(f"Part 1: {calc(data)}")
