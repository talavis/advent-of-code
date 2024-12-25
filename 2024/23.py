import requests

day = 23
part1 = True
part2 = True
testing = True
active = True

test_data = """
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""

test_data2 = test_data

test_ans1 = 7
test_ans2 = "co,de,ka,ta"


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row]
    return data


def calc(data):
    cons = {}
    for r in data:
        a, b = r.split("-")
        if a in cons:
            cons[a].add(b)
        else:
            cons[a] = {b}
        if b in cons:
            cons[b].add(a)
        else:
            cons[b] = {a}

    tgroups = set()
    for c in cons:
        if c[0] == "t":
            for a in cons[c]:
                for b in cons[a]:
                    if c in cons[b]:
                        tgroups.add(tuple(sorted([a, b, c])))

    return len(tgroups)


def calc2(data):
    def check_cons(group, cons):
        ok = True
        for a in group:
            for b in group:
                if not b in cons[a]:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            return group
        for i in range(len(group)):
            res = check_cons(group[:i] + group[i+1:], cons)
            if res:
                return res

    cons = {}
    for r in data:
        a, b = r.split("-")
        if a in cons:
            cons[a].add(b)
        else:
            cons[a] = {a, b}
        if b in cons:
            cons[b].add(a)
        else:
            cons[b] = {a, b}

    best = []
    for g in cons.values():
        res = check_cons(list(g), cons)
        if res and len(res) > len(best):
            best = res
    return ",".join(sorted(best))


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
        raw = requests.get(f"https://adventofcode.com/2024/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    if part1:
        data = parse(raw)
        print(f"Part 1: {calc(data)}")
    if part2:
        data = parse(raw)
        print(f"Part 2: {calc2(data)}")
