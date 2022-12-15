import functools
import requests

day = 11


def do_op(op, item):
    if op[2:] == "old":
        val = item
    else:
        val = int(op[2:])
    if op[0] == "*":
        return item * val
    if op[0] == "+":
        return item + val


def calc(data):
    score = 0
    monkeys = []
    for i in range(0, len(data), 6):
        monkeys.append(
            {
                "items": [int(item) for item in data[i + 1][18:].split(", ")],
                "op": data[i + 2][23:],
                "test": int(data[i + 3][21:]),
                "true": int(data[i + 4][29:]),
                "false": int(data[i + 5][30:]),
                "inspected": 0,
            }
        )

    import pprint

    for _ in range(20):
        for i, monkey in enumerate(monkeys):
            for item in monkey["items"]:
                monkey["inspected"] += 1
                worry = do_op(monkey["op"], item) // 3
                if worry % monkey["test"] == 0:
                    monkeys[monkey["true"]]["items"].append(worry)
                else:
                    monkeys[monkey["false"]]["items"].append(worry)
            monkey["items"] = []
    inspections = sorted([monkey["inspected"] for monkey in monkeys])
    return inspections[-1] * inspections[-2]


def calc2(data):
    monkeys = []
    for i in range(0, len(data), 6):
        monkeys.append(
            {
                "items": [int(item) for item in data[i + 1][18:].split(", ")],
                "op": data[i + 2][23:],
                "test": int(data[i + 3][21:]),
                "true": int(data[i + 4][29:]),
                "false": int(data[i + 5][30:]),
                "inspected": 0,
            }
        )

    max_tests = functools.reduce(lambda a, b: a * b, [m["test"] for m in monkeys])
    for r in range(10000):
        for i, monkey in enumerate(monkeys):
            for item in monkey["items"]:
                monkey["inspected"] += 1
                worry = do_op(monkey["op"], item) % max_tests
                if worry % monkey["test"] == 0:
                    monkeys[monkey["true"]]["items"].append(worry)
                else:
                    monkeys[monkey["false"]]["items"].append(worry)
            monkey["items"] = []
    inspections = sorted([monkey["inspected"] for monkey in monkeys])
    return inspections[-1] * inspections[-2]


test_data = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

test_data = [row for row in test_data.split("\n") if row]


res1 = calc(test_data)
res2 = calc2(test_data)
ans1 = 10605
ans2 = 2713310158
print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")
print(f"Test part 2: {res2} ({ans2}){'   !!!' if res2 != ans2 else ''}")

cookies = {"session": open("cookie.dat").read()}
req = requests.get(f"https://adventofcode.com/2022/day/{day}/input", cookies=cookies)
data_rows = req.text.split("\n")
data = [row for row in data_rows if row]

print(f"Part 1: {calc(data)}")
print(f"Part 2: {calc2(data)}")
