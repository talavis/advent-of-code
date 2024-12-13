import requests

day = 13
part1 = True
part2 = True
testing = True
active = True

test_data = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

test_data2 = test_data

test_ans1 = 480
test_ans2 = 0


def parse(indata):
    data_rows = indata.split("\n")
    data = [[]]
    for row in data_rows:
        if not row:
            if data[-1]:
                data.append([])
        else:
            pos = row.split(": ")[1]
            cols = pos.split(", ")
            if "+" in cols[0]:
                data[-1].append(
                    (int(cols[0].split("+")[1]), int(cols[1].split("+")[1]))
                )
            else:
                data[-1].append(
                    [int(cols[0].split("=")[1]), int(cols[1].split("=")[1])]
                )
    if not data[-1]:
        data.pop()
    return data


def calc(data):
    ans = 0
    for machine in data:
        pot = set()
        for a in range(101):
            for b in range(101):
                if (
                    machine[0][0] * a + machine[1][0] * b == machine[2][0]
                    and machine[0][1] * a + machine[1][1] * b == machine[2][1]
                ):
                    pot.add(3 * a + b)
                    break
                if (
                    machine[0][0] * a + machine[1][0] * b > machine[2][0]
                    or machine[0][1] * a + machine[1][1] * b > machine[2][1]
                ):
                    break
        if pot:
            ans += min(pot)
    return ans


def calc2(data):
    # a*ix + b*jx = kx
    # a*iy + b*jy = ky
    # ix*a + jx*b = kx
    # iy*a + jy*b = ky
    #
    # general solution form: 
    # a = (kx * jy - ky * jx) // (jy * ix - jx * iy)
    # b = (kx * iy - ky * ix) // (iy * jx - jy * ix)
    ans = 0
    for machine in data:
        machine[2][0] += 10000000000000
        machine[2][1] += 10000000000000
        ix, iy = machine[0]
        jx, jy = machine[1]
        kx, ky = machine[2]
        # a and must be integer -> integer division + check
        a = (kx * jy - ky * jx) // (jy * ix - jx * iy)
        b = (kx * iy - ky * ix) // (iy * jx - jy * ix)
        if ix * a + jx * b == kx and iy * a + jy * b == ky:
            ans += 3 * a + b

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
    cookies = {"session": open("cookie.dat").read()}
    try:
        raw = open(f"{day}.txt").read()
    except FileNotFoundError:
        raw = requests.get(
            f"https://adventofcode.com/2024/day/{day}/input", cookies=cookies
        ).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    if part1:
        data = parse(raw)
        print(f"Part 1: {calc(data)}")
    if part2:
        data = parse(raw)
        print(f"Part 2: {calc2(data)}")
