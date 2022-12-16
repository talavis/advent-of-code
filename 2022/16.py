import functools
import itertools
import multiprocessing as mp

import requests

day = 16


class Valve:
    def __init__(self, name, rate, conn):
        self.name = name
        self.rate = rate
        self.conn = conn

    def __repr__(self):
        return f"<Valve: {self.name}>"

    def __hash__(self):
        return hash(repr(self))


def parse(indata):
    data = []
    for row in indata:
        cols = row.split()
        name = cols[1]
        rate = int(cols[4].split("=")[1].strip(";"))
        conn = [entry.strip(",") for entry in cols[9:]]
        data.append(Valve(name, rate, conn))

    for val in data:
        for i, conn in enumerate(val.conn):
            for valv in data:
                if conn == valv.name:
                    val.conn[i] = valv
                    break
    return data


def add(active, current):
    return tuple(sorted(tuple(active) + (current,), key=lambda x: x.name))


@functools.lru_cache(maxsize=None)
def step1(t, current, active, n_rates):
    if len(active) == n_rates:
        return sum([v.rate for v in active]) * (30 - t)
    t += 1
    total = sum([v.rate for v in active])
    if t == 30:
        return total
    best = 0
    if current.rate > 0 and current not in active:
        res = step1(t, current, add(active, current), n_rates)
        if res > best:
            best = res
    for conn in current.conn:
        res = step1(t, conn, active, n_rates)
        if res > best:
            best = res
    return total + best


def calc(indata):
    data = parse(indata)
    for valve in data:
        if valve.name == "AA":
            current = valve
            break

    n_rates = len([val for val in data if val.rate > 0])
    active = tuple()
    total = step1(0, current, active, n_rates)

    return total


def run_both(current, comb, remain, A_MAX):
    @functools.lru_cache(maxsize=None)
    def step2(t, current, active, remain):
        if len(active) == A_MAX:
            return sum([v.rate for v in active]) * (26 - t)
        t += 1
        total = sum([v.rate for v in active])
        if t == 26:
            return total
        best = 0
        if current.rate > 0 and current not in active and current not in remain:
            res = step2(t, current, add(active, current), remain)
            if res > best:
                best = res
        for conn in current.conn:
            res = step2(t, conn, active, remain)
            if res > best:
                best = res
        return total + best

    return step2(0, current, tuple(), remain) + step2(0, current, tuple(), comb)


def calc2(indata, pool):
    data = parse(indata)
    for valve in data:
        if valve.name == "AA":
            current = valve
            break
    r_valves = {val for val in data if val.rate > 0}
    best = 0
    done = set()
    for i in range(len(r_valves) + 1):
        results = []
        combs = itertools.combinations(r_valves, i)
        print(i)
        for comb in combs:
            done.add(comb)
            remain = set(r_valves)
            for val in comb:
                remain.remove(val)
            A_MAX = len(r_valves) - len(remain)
            remain = tuple(remain)
            active = tuple()
            if remain not in done:
                results.append(pool.apply_async(run_both, args=(current, comb, remain, A_MAX)))
        for result in results:
            score = result.get()
            if score > best:
                best = score
                print(best)
    return best


if __name__ == "__main__":
    test_data = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

    test_data = [row for row in test_data.split("\n") if row]

    res1 = calc(test_data)

    with mp.Pool(mp.cpu_count()) as p:
        res2 = calc2(test_data, p)

    ans1 = 1651
    ans2 = 1707
    print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")

    with mp.Pool(mp.cpu_count()) as p:
        print(f"Test part 2: {res2} ({ans2}){'   !!!' if res2 != ans2 else ''}")

    active = True
    if active:
        cookies = {"session": open("cookie.dat").read()}
        req = requests.get(f"https://adventofcode.com/2022/day/{day}/input", cookies=cookies).text
        # req =  open(f"{day}.txt").read()
        data_rows = req.split("\n")
        data = [row for row in data_rows if row]

        print(f"Part 1: {calc(data)}")
        with mp.Pool(mp.cpu_count()) as p:
            print(f"Part 2: {calc2(data, p)}")
