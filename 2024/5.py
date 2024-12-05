import collections

import requests

day = 5
part1 = True
part2 = True
testing = True
active = True

test_data = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

test_data2 = test_data

test_ans1 = 143
test_ans2 = 123


def parse(indata):
    data_rows = indata.split("\n")
    orders = {}
    updates = []
    second = False
    for row in data_rows:
        if not row:
            if len(orders):
                second = True
            continue
        if not second:
            cols = row.split("|")
            k = int(cols[0])
            v = int(cols[1])
            if k not in orders:
                orders[k] = {v}
            else:
                orders[k].add(v)
        else:
            updates.append([int(i) for i in row.split(",")])

    return (orders, updates)


def calc(data):
    orders = data[0]
    updates = data[1]

    ans = 0
    
    for update in updates:
        correct = True
        for i in range(len(update)):
            for j in range(i+1, len(update)):
                if update[j] not in orders:
                    orders[update[j]] = {}
                if update[i] not in orders:
                    orders[update[i]] = {}
                if update[j] not in orders[update[i]]:
                    correct = False
                    break
            if not correct:
                break
        if correct:
            ans += update[len(update)//2]
    return ans


def calc2(data):
    orders = data[0]
    updates = data[1]

    ans = 0
    
    for update in updates:
        correct = True
        for i in range(len(update)):
            for j in range(i+1, len(update)):
                if update[j] not in orders:
                    orders[update[j]] = {}
                if update[i] not in orders:
                    orders[update[i]] = {}
                if update[j] not in orders[update[i]]:
                    correct = False
                    break
            if not correct:
                break
        if not correct:
            new_update = update[:]
            i = 0
            while i < len(new_update):
                swapped = False
                for j in range(i, len(new_update)):
                    if new_update[i] in orders[new_update[j]]:
                        a = new_update[j]
                        new_update[j] = new_update[i]
                        new_update[i] = a
                        swapped = True
                if not swapped:
                    i += 1
            ans += new_update[len(new_update)//2]            
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
        raw = requests.get(f"https://adventofcode.com/2024/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    if part1:
        data = parse(raw)
        print(f"Part 1: {calc(data)}")
    if part2:
        data = parse(raw)
        print(f"Part 2: {calc2(data)}")
