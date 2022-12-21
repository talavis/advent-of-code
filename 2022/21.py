import copy

import requests

day = 21
part1 = True
part2 = True
testing = True
active = True

class Monkey:
    def __init__(self, name, cols):
        self.name = name
        if len(cols) == 1:
            self.shout = int(cols[0])
            self.monk1 = None
            self.monk2 = None
            self.op = None
        else:
            self.shout = None
            self.monk1 = cols[0]
            self.monk2 = cols[2]
            self.op = cols[1]

    def __repr__(self):
        return f"<{self.name} s={self.shout}>"
            
    def value(self, ref):
        if self.shout is None:
            if self.op == "+":
                val = ref[self.monk1].value(ref) + ref[self.monk2].value(ref)
            elif self.op == "-":
                val = ref[self.monk1].value(ref) - ref[self.monk2].value(ref)
            elif self.op == "*":
                val = ref[self.monk1].value(ref) * ref[self.monk2].value(ref)
            elif self.op == "/":  # assume whole integers
                val = ref[self.monk1].value(ref) / ref[self.monk2].value(ref)
            elif self.op == "=":
#                print(ref[self.monk1].value(ref), ref[self.monk2].value(ref), ref[self.monk1].value(ref)-ref[self.monk2].value(ref))
                return (ref[self.monk1].value(ref), ref[self.monk2].value(ref))
            self.shout = val
        return self.shout


def parse(indata):
    data_rows = indata.split("\n")
    data = {}
    for row in data_rows:
        if not row.strip():
            continue
        cols = row.split()
        name = cols[0][:-1]
        data[name] = Monkey(name, cols[1:])
    return data


def calc(data):
    data = copy.deepcopy(data)
    val = data["root"].value(data)
    return int(val)


def calc2(data):
    data["root"].op = "="
    orig = copy.deepcopy(data)

    data["humn"].shout = 0
    res = data["root"].value(data)
    diff = res[0]-res[1]
    if diff < 0:
        reverse = True
    else:
        reverse = False
    # assumes res[0] > res[1], res[1] is unchanged, which was true for test data and my input
    l = 0
    h = 10*abs(diff)  # arbitrary start number
    while diff != 0:
        mid = l+(h-l)//2
        data = copy.deepcopy(orig)
        data["humn"].shout = mid
        res = data["root"].value(data)
        if reverse:
            diff = res[1]-res[0]
        else:
            diff = res[0]-res[1]
        if diff > 0:
            l = mid
        elif diff < 0:
            h = mid
    return int(mid)


test_data = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""

if testing:
    test_data = parse(test_data)

    if part1:
        res1 = calc(test_data)
        ans1 = 152
        print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")
    if part2:
        res2 = calc2(test_data)
        ans2 = 301
        print(f"Test part 2: {res2} ({ans2}){'   !!!' if res2 != ans2 else ''}")

if active:
    cookies = {"session": open("cookie.dat").read()}
    try:
        raw = open(f"{day}.txt").read()
    except FileNotFoundError:
        raw = requests.get(f"https://adventofcode.com/2022/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    data = parse(raw)
    if part1:
        print(f"Part 1: {calc(data)}")
    if part2:
        print(f"Part 2: {calc2(data)}")
