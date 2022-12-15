import time

start = time.time()
data = open("1.dat").read().split("\n")

elves = [0]
for row in data:
    if not row:
        elves.append(0)
        continue
    elves[-1] += int(row)

res1 = max(elves)

elves.sort()

res2 = sum(elves[-3:])

end = time.time()

print(res1)
print(res2)

print(f"Runtime: {end-start} seconds")
