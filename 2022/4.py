def calc(data):
    score = 0
    for row in data:
        first = row[0].split("-")
        first = int(first[0]), int(first[1])
        second = row[1].split("-")
        second = int(second[0]), int(second[1])
        if first[0] <= second[0] and first[1] >= second[1]:
            score += 1
            continue
        if first[0] >= second[0] and first[1] <= second[1]:
            score += 1
    return score


def calc2(data):
    score = 0
    for row in data:
        first = row[0].split("-")
        first = int(first[0]), int(first[1])
        second = row[1].split("-")
        second = int(second[0]), int(second[1])
        if not (second[1] < first[0] or first[1] < second[0]):
            score += 1
    return score


test_data = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

test_data = [row.split(",") for row in test_data.split("\n") if row]

print(f"Test part 1: {calc(test_data)} (should be 2)")
print(f"Test part 2: {calc2(test_data)} (should be 4)")

data = [row.split(",") for row in open("4.dat").read().split("\n") if row]

print(f"Part 1: {calc(data)}")
print(f"Part 2: {calc2(data)}")
