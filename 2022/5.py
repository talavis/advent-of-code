def calc(data):
    stacks = []
    started = False
    for row in data:
        if not started:
            # load stacks
            for i in range(1, len(row), 4):
                if row[i] == "1":
                    started = True
                    for i in range(len(stacks)):  # flip the stacks to enable use of .pop()
                        stacks[i] = stacks[i][::-1]
                    break
                if i // 4 >= len(stacks):
                    stacks.append([])
                if row[i].strip():
                    stacks[i // 4].append(row[i])
            continue
        if started:
            # move stacks
            cols = row.split()
            amount = int(cols[1])
            sfrom = int(cols[3]) - 1
            sto = int(cols[5]) - 1

            for _ in range(amount):
                crate = stacks[sfrom].pop()
                stacks[sto].append(crate)

    end = ""
    for stack in stacks:
        if stack:
            end += stack[-1]
    return end


def calc2(data):
    stacks = []
    started = False
    for row in data:
        if not started:
            # load stacks
            for i in range(1, len(row), 4):
                if row[i] == "1":
                    started = True
                    for i in range(len(stacks)):  # flip the stacks to enable use of .pop()
                        stacks[i] = stacks[i][::-1]
                    break
                if i // 4 >= len(stacks):
                    stacks.append([])
                if row[i].strip():
                    stacks[i // 4].append(row[i])
            continue
        if started:
            # move stacks
            cols = row.split()
            amount = int(cols[1])
            sfrom = int(cols[3]) - 1
            sto = int(cols[5]) - 1

            tmpstack = []
            for _ in range(amount):
                crate = stacks[sfrom].pop()
                tmpstack.append(crate)
            for _ in range(amount):
                crate = tmpstack.pop()
                stacks[sto].append(crate)

    end = ""
    for stack in stacks:
        if stack:
            end += stack[-1]
    return end


test_data = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

test_data = [row for row in test_data.split("\n") if row]

print(f"Test part 1: {calc(test_data)} (CMZ)")
print(f"Test part 2: {calc2(test_data)} (MCD)")

data = [row for row in open("5.dat").read().split("\n") if row]

print(f"Part 1: {calc(data)}")

print(f"Part 2: {calc2(data)}")
