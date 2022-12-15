import requests

day = 15


def parse(indata):
    data = []
    for row in indata:
        cols = row.split()
        sensor = [int(cols[2].split("=")[1][:-1]), int(cols[3].split("=")[1][:-1])]
        beacon = [int(cols[8].split("=")[1][:-1]), int(cols[9].split("=")[1])]
        data.append([sensor, beacon])
    return data


def find_blockers(y, sensors, beacons, only_pos=True):
    blockers = []
    for sen in sensors:
        ydist = abs(y - sen[1])
        if ydist < sen[2]:
            start = sen[0] - (sen[2] - ydist)
            end = sen[0] + (sen[2] - ydist)
            if only_pos:
                if start < 0:
                    start = 0
                if end >= 0:
                    blockers.append([start, end])
            else:
                blockers.append([start, end])
    for bea in beacons:
        if bea[1] == y and bea[0] > 0:
            blockers.append([bea[1], bea[1]])
    blockers.sort(key=lambda x: x[0])
    i = 0
    while i < len(blockers) - 1:
        if blockers[i][1] >= blockers[i + 1][1]:
            blockers.pop(i + 1)
        elif blockers[i][1] >= blockers[i + 1][0] and blockers[i][1] < blockers[i + 1][1]:
            blockers[i][1] = blockers[i + 1][1]
            blockers.pop(i + 1)
        else:
            i += 1
    return blockers


def calc(indata, target=2000000):
    data = parse(indata)
    sensors = [
        (row[0][0], row[0][1], abs(row[0][0] - row[1][0]) + abs(row[0][1] - row[1][1]))
        for row in data
    ]
    beacons = [tuple(row[1]) for row in data]
    blockers = find_blockers(target, sensors, beacons, only_pos=False)
    n_blocked = 0
    for blo in blockers:
        n_blocked += blo[1] - blo[0]
    return n_blocked


def calc2(indata, target=4000000):
    data = parse(indata)
    hits = set()
    sensors = [
        (row[0][0], row[0][1], abs(row[0][0] - row[1][0]) + abs(row[0][1] - row[1][1]))
        for row in data
    ]
    beacons = [tuple(row[1]) for row in data]
    for y in range(0, target + 1):
        blockers = find_blockers(y, sensors, beacons)
        if blockers[0][0] != 0:
            return y
        elif blockers[0][1] < target:
            return (blockers[0][1] + 1) * 4000000 + y

    return -1


test_data = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

test_data = [row for row in test_data.split("\n") if row]


res1 = calc(test_data, 10)
res2 = calc2(test_data, 20)
ans1 = 26
ans2 = 56000011
print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")
print(f"Test part 2: {res2} ({ans2}){'   !!!' if res2 != ans2 else ''}")

active = True
if active:
    cookies = {"session": open("cookie.dat").read()}
    req = requests.get(f"https://adventofcode.com/2022/day/{day}/input", cookies=cookies).text
    # req =  open(f"{day}.txt").read()
    data_rows = req.split("\n")
    data = [row for row in data_rows if row]

    print(f"Part 1: {calc(data)}")
    print(f"Part 2: {calc2(data)}")
