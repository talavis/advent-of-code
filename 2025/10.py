import itertools
import time

import requests
import z3

day = 10
part1 = True
part2 = True
testing = True
active = True
timings = False

test_data = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""

test_data2 = test_data

test_ans1 = 7
test_ans2 = 33


def parse(indata):
    data_rows = indata.split("\n")
    lights = []
    buttons = []
    joltages = []
    for row in data_rows:
        if not row:
            continue
        cols = row.split()
        lights.append([int(val == "#") for val in cols[0][1:-1]])
        buttons.append([])
        for button in cols[1:-1]:
            buttons[-1].append([int(val) for val in button[1:-1].split(",")])
        joltages.append([int(val) for val in cols[-1][1:-1].split(",")])
    return lights, buttons, joltages


def calc(data):
    def find_best(light, combos):
        # assume never more than 8 button presses
        for j in range(1, 8):
            for combo in itertools.combinations_with_replacement(combos, j):
                current = [0]*len(light)
                for press in combo:
                    for button in press:
                        current[button] = (current[button] + 1) % 2
                if current == light:
                    return j

    lights, buttons, _ = data

    ans = 0
    for i in range(len(lights)):
        ans += find_best(lights[i], buttons[i])
        
    return ans


def calc2(data):
    # solved using z3
    # mostly by adapting tutorials
    _, button_groups, joltages = data
    ans = 0
    
    for i in range(len(button_groups)):
        buttons = button_groups[i]
        joltage = joltages[i]

        # equation representations for the buttons
        groups = []
        for i in range(len(buttons)):
            groups.append(z3.Int(f'B{i}'))

        # generate the equations that should be solved
        equations = []
        for i in range(len(joltage)):
            terms = []
            for j in range(len(buttons)):
                if i in buttons[j]:
                    terms.append(groups[j])
            eq = (sum(terms) == joltage[i])
            equations.append(eq)

        # use z3 to solve the equations
        optimiser = z3.Optimize()
        optimiser.minimize(sum(groups))
        for equation in equations:
            optimiser.add(equation)
        for group in groups:
            optimiser.add(group >= 0)
        assert optimiser.check()
        model = optimiser.model()
        for d in model.decls():
            ans += model[d].as_long()
        
    return ans


start_total = time.perf_counter()
if testing:
    if part1:
        start_test_part1 = time.perf_counter()
        test_data_p = parse(test_data)
        res1 = calc(test_data_p)
        end_test_part1 = time.perf_counter()
        print(
            f"Test part 1: {res1} ({test_ans1}){'   !!!' if res1 != test_ans1 else ''}"
        )

    if part2:
        start_test_part2 = time.perf_counter()
        test_data_p2 = parse(test_data2)
        res2 = calc2(test_data_p2)
        end_test_part2 = time.perf_counter()
        print(
            f"Test part 2: {res2} ({test_ans2}){'   !!!' if res2 != test_ans2 else ''}"
        )

if active:
    with open("cookie.dat") as f:
        cookies = {"session": f.read()}
    try:
        with open(f"{day}.txt") as f:
            raw = f.read()
    except FileNotFoundError:
        raw = requests.get(
            f"https://adventofcode.com/2025/day/{day}/input", cookies=cookies
        ).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    if part1:
        start_part1 = time.perf_counter()
        data = parse(raw)
        ans = calc(data)
        end_part1 = time.perf_counter()
        print(f"Part 1: {ans}")

    if part2:
        start_part2 = time.perf_counter()
        data = parse(raw)
        ans = calc2(data)
        end_part2 = time.perf_counter()
        print(f"Part 2: {ans}")

end_total = time.perf_counter()

if timings:
    print("Runtime:")
    if part1:
        if testing:
            print(f"Test 1: {end_test_part1 - start_test_part1} seconds")
        if active:
            print(f"Part 1: {end_part1 - start_part1} seconds")
    if part2:
        if testing:
            print(f"Test 2: {end_test_part2 - start_test_part2} seconds")
        if active:
            print(f"Part 2: {end_part2 - start_part2} seconds")
    print(f"Total: {end_total - start_total} seconds")
