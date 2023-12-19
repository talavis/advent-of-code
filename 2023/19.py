import requests

day = 19
part1 = True
part2 = True
testing = True
active = True

test_data = """
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""

test_data2 = test_data

test_ans1 = 19114
test_ans2 = 167409079868000


def parse(indata):
    data_rows = indata.split("\n")
    wf = {}
    data = []
    d_started = False
    v_pos = "xmas"
    for r in data_rows:
        if wf and not r:
            d_started = True
            continue
        if d_started:
            data.append([int(e[e.index("=") + 1 :]) for e in r[1:-1].split(",")])
        elif r:
            name = r[: r.index("{")]
            rules = []
            # [o, vi, num, go]
            for p in r[r.index("{") + 1 : -1].split(","):
                gt = ">" in p
                lt = "<" in p
                vi = -1
                if gt or lt:
                    vi = v_pos.index(p[0])
                    go = p[p.index(":") + 1 :]
                    if gt:
                        num = int(p[p.index(">") + 1 : p.index(":")])
                        rules.append([">", vi, num, go])
                    elif lt:
                        num = int(p[p.index("<") + 1 : p.index(":")])
                        rules.append(["<", vi, num, go])
                else:
                    go = p
                    rules.append(["", -1, -1, go])
            wf[name] = rules

    return wf, data


def calc(data):
    wf, data = data
    score = 0
    for d in data:
        res = ""
        for r in wf["in"]:
            if r[0] == ">":
                if d[r[1]] > r[2]:
                    res = r[3]
                    break
            elif r[0] == "<":
                if d[r[1]] < r[2]:
                    res = r[3]
                    break
            else:
                res = r[3]
        while res not in ("A", "R"):
            for r in wf[res]:
                if r[0] == ">":
                    if d[r[1]] > r[2]:
                        res = r[3]
                        break
                elif r[0] == "<":
                    if d[r[1]] < r[2]:
                        res = r[3]
                        break
                else:
                    res = r[3]
                    break
        if res == "A":
            score += sum(d)

    return score


def calc2(data):
    wf = data[0]

    def travel(wf_name, values):
        if wf_name == "A":
            m = 1
            for v in values:
                m *= v[1] - v[0] + 1
            return m
        if wf_name == "R":
            return 0
        res = 0
        for r in wf[wf_name]:
            if r[0] == ">":
                if values[r[1]][1] > r[2]:
                    new_values = [list(a) for a in values]
                    new_values[r[1]][0] = r[2] + 1
                    values[r[1]][1] = r[2]
                    res += travel(r[3], new_values)
            elif r[0] == "<":
                if values[r[1]][0] < r[2]:
                    new_values = [list(a) for a in values]
                    new_values[r[1]][1] = r[2] - 1
                    values[r[1]][0] = r[2]
                    res += travel(r[3], new_values)
            else:
                new_values = [list(a) for a in values]
                res += travel(r[3], new_values)
        return res

    vals = [[1, 4000], [1, 4000], [1, 4000], [1, 4000]]
    res = travel("in", vals)

    return res


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
        raw = requests.get(f"https://adventofcode.com/2023/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    if part1:
        data = parse(raw)
        print(f"Part 1: {calc(data)}")
    if part2:
        data = parse(raw)
        print(f"Part 2: {calc2(data)}")
