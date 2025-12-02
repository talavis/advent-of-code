import requests

day = 2
part1 = True
part2 = True
testing = True
active = True

test_data = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""

test_data2 = test_data

test_ans1 = 1227775554
test_ans2 = 4174379265


def parse(indata):
    data_rows = indata.split("\n")
    data = [(int(parts[0:parts.index("-")]), int(parts[parts.index("-")+1:])) for parts in data_rows[0].split(",") if parts]
    return data


def calc(data):
    def gen(base, r, hits):
        for i in range(10):
            new_base = base + str(i)
            if not int(new_base):
                continue
            if r[0] <= int(2*new_base) <= r[1]:
                hits.add(int(2*new_base))
            if int(2*new_base) > r[1]:
                break
            gen(new_base, r, hits)
            
        return hits
    
    hits = set()
    for r in data:
        gen("", r, hits)
    return sum(hits)


def calc2(data):
    def gen(base, r, hits):
        for i in range(10):
            new_base = base + str(i)
            if not int(new_base):
                continue
            j = 2
            while int(j*new_base) <= r[1]:
                if r[0] <= int(j*new_base) <= r[1]:
                    hits.add(int(j*new_base))
                j += 1
            if int(2*new_base) > r[1]:
                break
            gen(new_base, r, hits)
        return hits
    
    hits = set()
    for r in data:
        gen("", r, hits)
    return sum(hits)


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
    with open("cookie.dat") as f:
        cookies = {"session": f.read()}
    try:
        with open(f"{day}.txt") as f:
            raw = f.read()
    except FileNotFoundError:
        raw = requests.get(f"https://adventofcode.com/2025/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    if part1:
        data = parse(raw)
        print(f"Part 1: {calc(data)}")
    if part2:
        data = parse(raw)
        print(f"Part 2: {calc2(data)}")
