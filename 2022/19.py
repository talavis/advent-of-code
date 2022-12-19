import functools
import requests

day = 19
testing = True
active = True


def parse(raw):
    rows = raw.split("\n")
    robots = []
    for row in rows:
        if len(row) < 4:
            continue
        cols = row.split(".")
        robots.append({
            "id": int(cols[0].split()[1].strip(":")),
            "ore": int(cols[0].split()[6]),
            "clay": int(cols[1].split()[4]),
            "obs": (int(cols[2].split()[4]),
                         int(cols[2].split()[7])),
            "geo": (int(cols[3].split()[4]),
                       int(cols[3].split()[7])),
        })
    return robots


def new_res(res, rob):
    return (res[0]+rob[0],
            res[1]+rob[1],
            res[2]+rob[2],
            res[3]+rob[3])


def stepper(bp, end):
    """
    Assumptions:
    [1] only 1 robot can be built every step
    [2] due to [1], there is no reason to produce more of the "simpler" types
        once there's enough to produce a copy of any (all) of the more complex types    
    [3] a robot is always built if the nr of ores > 6 (arbitrary, but worked)
    """
    @functools.cache
    def step(res, rob, s, end):
        if s == end:
            return res[3]
        reso = new_res(res, rob)
        results = [0]
        # assumption: always build geode robot if possible
        if res[0] >= bp["geo"][0] and res[2] >= bp["geo"][1]:
            results.append(step(
                (reso[0]-bp["geo"][0], reso[1], reso[2]-bp["geo"][1], reso[3]),
                (rob[0], rob[1], rob[2], rob[3]+1),
                s+1,
                end
            ))
        else:
            if res[0] >= bp["obs"][0] and res[1] >= bp["obs"][1]:
                if bp["geo"][1] > rob[2]:
                    results.append(step(
                        (reso[0]-bp["obs"][0], reso[1]-bp["obs"][1], reso[2], reso[3]),
                        (rob[0], rob[1], rob[2]+1, rob[3]),
                        s+1,
                        end
                    ))
            if res[0] >= bp["clay"]:
                if bp["obs"][1] > rob[1] and bp["geo"][1] > rob[2]:
                    results.append(step(
                        (reso[0]-bp["clay"], reso[1], reso[2], reso[3]),
                        (rob[0], rob[1]+1, rob[2], rob[3]),
                        s+1,
                        end
                    ))
            if res[0] >= bp["ore"]:
                if max(bp["clay"], bp["obs"][0], bp["geo"][0]) > rob[0]:
                    results.append(step(
                        (reso[0]-bp["ore"], reso[1], reso[2], reso[3]),
                        (rob[0]+1, rob[1], rob[2], rob[3]),
                        s+1,
                        end
                    ))
            # arbitratry limit to decrease the space that has to explored
            # might need to be changed for other data
            if res[0] < 7:
                results.append(step(reso, rob, s+1, end))

        return max(results)

    resources = (0, 0, 0, 0)
    robots = (1, 0, 0, 0)
    return step(resources, robots, 0, end)
    

def calc(data):
    score = 0
    for bp in data:
        res = stepper(bp, 24)
        score += bp["id"]*res
    return score


def calc2(data):
    score = 1
    for bp in data[:3]:
        res = stepper(bp, 32)
        print(bp["id"], res)
        score *= res
    return score


test_data = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2:  Each ore robot costs 2 ore.  Each clay robot costs 3 ore.  Each obsidian robot costs 3 ore and 8 clay.  Each geode robot costs 3 ore and 12 obsidian."""

test_data = parse(test_data)

if testing:
    res1 = calc(test_data)
    res2 = calc2(test_data)
    ans1 = 33
    ans2 = 3472
    print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")
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
    print(f"Part 1: {calc(data)}")
    print(f"Part 2: {calc2(data)}")
