def calc(data):
    score = 0
    for row in data:
        comp1 = row[:len(row)//2]
        comp2 = row[len(row)//2:]
        both = ""
        for c in comp1:
            if c in comp2:
                break

        if ord(c) < ord("a"):
            score += ord(c)-ord("A")+27
        else:
            score += ord(c)-ord("a")+1
    return score


def calc2(data):
    score = 0
    for i in range(0, len(data), 3):
        for c in data[i]:
            if c in data[i+1]:
                if c in data[i+2]:
                    break
        if ord(c) < ord("a"):
            score += ord(c)-ord("A")+27
        else:
            score += ord(c)-ord("a")+1
    
    return score


test_data = ["vJrwpWtwJgWrhcsFMMfFFhFp",
             "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
             "PmmdzqPrVvPwwTWBwg",
             "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
             "ttgJtRGJQctTZtZT",
             "CrZsJsPPZsGzwwsLwLmpwMDw"]

print(f"Test: {calc(test_data)} (should be 157)")
print(f"Test: {calc2(test_data)} (should be 70)")

data = [row for row in open("3.dat").read().split("\n") if row]

res1 = calc(data)
print(f"Part 1: {res1}")

res2 = calc2(data)
print(f"Part 2: {res2}")
