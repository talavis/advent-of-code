import requests

day = 5
part1 = True
part2 = True
testing = True
active = True

test_ans1 = 35
test_ans2 = 46

test_data = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

order = ["seeds", "s-s", "s-f", "f-w", "w-l", "l-t", "t-h", "h-l"]


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row]
    mapper = {}
    o = -1
    mapper["seeds"] = [int(val) for val in data[0][data[0].index(":") + 1 :].split()]
    for row in data:
        if ":" in row:
            o += 1
            if order[o] not in mapper:
                mapper[order[o]] = []
            continue
        vals = [int(val) for val in row.split()]
        mapper[order[o]].append((vals[1], vals[1] + vals[2], vals[0] - vals[1]))
    return mapper


def calc(mapper):
    def convert(val, mappers):
        for mapper in mappers:
            if val >= mapper[0] and val < mapper[1]:
                return val + mapper[2]
        return val

    o = 1
    values = [val for val in mapper["seeds"]]
    while o < len(order):
        for i in range(len(values)):
            values[i] = convert(values[i], mapper[order[o]])
        o += 1
    return min(values)


def calc2(mapper):
    best = float("inf")
    for o in range(1, len(order)):
        mapper[order[o]].sort()
    for i in range(0, len(mapper["seeds"]), 2):
        # initial seed range
        ranges = [[mapper["seeds"][i], mapper["seeds"][i] + mapper["seeds"][i + 1]]]
        # for each conversion
        for o in range(1, len(order)):
            new_ranges = []
            for r in ranges:
                mi = r[0]
                ma = r[1]
                i = 0
                for m in mapper[order[o]]:
                    # special range started before
                    if m[0] <= mi < m[1]:
                        # covered by entire special range
                        if ma < m[1]:
                            new_ranges.append([mi + m[2], ma + m[2]])
                            mi = ma
                        # special range ends inside
                        else:
                            new_ranges.append([mi + m[2], m[1] + m[2]])
                            mi = m[1]
                    # special range starts inside
                    if mi <= m[0] < ma:
                        # before special range starts
                        new_ranges.append([mi, m[0]])
                        mi = m[0]
                        # special range ends inside
                        if m[1] < ma:
                            new_ranges.append([m[0] + m[2], m[1] + m[2]])
                            mi = m[1]
                        # special range covers end of range
                        else:
                            new_ranges.append([m[0] + m[2], ma + m[2]])
                            mi = ma
                # trailing end of range
                if mi != ma:
                    new_ranges.append([mi, ma])
            ranges = new_ranges
            ranges.sort()
        if best > ranges[0][0]:
            best = ranges[0][0]
    return best


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
