def calc_score(data, scores):
    total = 0
    for row in data:
        total += scores[row[0]][row[1]]
    return total


scores_1 = {
    "A": {"X": 4, "Y": 8, "Z": 3},
    "B": {"X": 1, "Y": 5, "Z": 9},
    "C": {"X": 7, "Y": 2, "Z": 6},
}

scores_2 = {
    "A": {"X": 3, "Y": 4, "Z": 8},
    "B": {"X": 1, "Y": 5, "Z": 9},
    "C": {"X": 2, "Y": 6, "Z": 7},
}

test_data = [("A", "Y"), ("B", "X"), ("C", "Z")]

print(f"Test: {calc_score(test_data, scores_1)} (should be 15)")
print(f"Test: {calc_score(test_data, scores_2)} (should be 12)")


data = [row.split() for row in open("2.dat").read().split("\n") if row]

res1 = calc_score(data, scores_1)
print(res1)

res2 = calc_score(data, scores_2)
print(res2)
