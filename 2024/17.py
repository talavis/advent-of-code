import requests

day = 17
part1 = True
part2 = True
testing = True
active = True

test_data = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""

test_data2 = """
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""

test_ans1 = "4,6,3,5,6,3,5,2,1,0"
test_ans2 = 117440


def parse(indata):
    reg_raw, prog_raw = [part for part in indata.split("\n\n") if part]
    registers = [int(row.split(": ")[1]) for row in reg_raw.split("\n") if row]
    program = [int(val) for val in prog_raw.split(":")[1].split(",")]
    return registers, program


def calc(data):
    registers, program = data
    out = []

    def combo(operand):
        if 0 < operand <= 3:
            return operand
        if 4 <= operand <= 6:
            return registers[operand - 4]
        raise KeyError("should not occur")

    def op(pos):
        match program[pos]:
            case 0:
                registers[0] = registers[0] // (2 ** combo(program[pos + 1]))
            case 1:
                registers[1] = registers[1] ^ program[pos + 1]
            case 2:
                registers[1] = combo(program[pos + 1]) % 8
            case 3:
                if registers[0]:
                    pos = program[pos + 1] - 2  # since it will be increased by two
            case 4:
                registers[1] = registers[1] ^ registers[2]
            case 5:
                out.append(combo(program[pos + 1]) % 8)
            case 6:
                registers[1] = registers[0] // (2 ** combo(program[pos + 1]))
            case 7:
                registers[2] = registers[0] // (2 ** combo(program[pos + 1]))
        pos += 2
        return pos

    pos = 0
    while 0 <= pos < len(program):
        pos = op(pos)

    return ",".join(str(v) for v in out)


def calc2(data: tuple):
    _, program = data

    def run(registers: list):
        out = []

        def combo(operand):
            if 0 < operand <= 3:
                return operand
            if 4 <= operand <= 6:
                return registers[operand - 4]
            raise KeyError("should not occur")

        def op(pos):
            match program[pos]:
                case 0:
                    registers[0] = registers[0] // (2 ** combo(program[pos + 1]))
                case 1:
                    registers[1] = registers[1] ^ program[pos + 1]
                case 2:
                    registers[1] = combo(program[pos + 1]) % 8
                case 3:
                    if registers[0]:
                        pos = program[pos + 1] - 2  # since it will be increased by two
                case 4:
                    registers[1] = registers[1] ^ registers[2]
                case 5:
                    out.append(combo(program[pos + 1]) % 8)
                case 6:
                    registers[1] = registers[0] // (2 ** combo(program[pos + 1]))
                case 7:
                    registers[2] = registers[0] // (2 ** combo(program[pos + 1]))
            pos += 2
            return pos

        pos = 0
        while 0 <= pos < len(program):
            pos = op(pos)
        return out

    def find_input(pos, start):
        """
        Build the wanted result, starting from the right.

        As the operations are %8, it should be fine to raise the value by eight times.
        """

        for i in range(8):
            out = run([start * 8 + i, 0, 0])
            if program[pos:] == out:
                if pos == 0:
                    return start * 8 + i
                ans = find_input(pos - 1, start * 8 + i)
                if ans is not None:
                    return ans
        return None

    return find_input(len(program) - 1, 0)


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
