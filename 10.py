import requests

day = 10

def calc(data):
    score = 0
    x = 1
    c = 1
    for row in data:
        cols = row.split()
        if (c-20)%40 == 0:
            score += c*x
        if cols[0] == "addx":
            if (c-20+1)%40 == 0:
                score += (c+1)*x
            x += int(cols[1])
            c += 2
        elif row == "noop":
            c += 1
    while c < 220:
        if (c)%20 == 0:
            score += x
        c += 1
    return score


def calc2(data, out=True):
    cycles = [0]*240
    c = 0
    x = 1
    for row in data:
        cycles[c] = x
        cols = row.split()
        if cols[0] == "addx":
            cycles[c+1] = x
            x += int(cols[1])
            c += 2
        elif row == "noop":
            c += 1
    while c < 240:
        cycles[c] = x
        c += 1

    screen = ["."]*240
    for i in range(240):
        val = cycles[i]
        if val-1 <= i%40 <= val+1:
            screen[i] = "#"

    if out:
        for i in range(0, 240, 40):
            print("".join(screen[i:i+40]))
    return "".join(screen)


test_data = open("10_test.dat").read()
test_data = [row for row in test_data.split("\n") if row]

res1 = calc(test_data)
res2 = calc2(test_data, False)
ans1 = 13140
ans2 = ("##..##..##..##..##..##..##..##..##..##.."
        "###...###...###...###...###...###...###."
        "####....####....####....####....####...."
        "#####.....#####.....#####.....#####....."
        "######......######......######......####"
        "#######.......#######.......#######.....")
print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")
print(f"Test part 2: {'Pass' if res2 == ans2 else 'Fail'}")

cookies = {"session": open("cookie.dat").read()}
req = requests.get(f"https://adventofcode.com/2022/day/{day}/input", cookies=cookies)
data_rows = req.text.split("\n")
data = [row for row in data_rows if row]

print(f"Part 1: {calc(data)}")
print("Part 2:")
calc2(data)
