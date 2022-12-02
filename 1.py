data = open("1.dat").read().split("\n")

elves = [0]
for row in data:
    if not row:
        elves.append(0)
        continue
    elves[-1] += int(row)

print(max(elves))

total = 0
for i in range(3):
    total += max(elves)
    elves.pop(elves.index(max(elves)))

print(total)
