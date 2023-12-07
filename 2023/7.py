from functools import cmp_to_key
from collections import Counter

import requests

day = 7
part1 = True
part2 = True
testing = True
active = True

test_ans1 = 6440
test_ans2 = 5905

test_data = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""


def parse(indata):
    data_rows = indata.split("\n")
    data = [row.split() for row in data_rows if row]
    data = [[entry[0], int(entry[1])] for entry in data]
    return data


def calc(data):
    def compare(hand1, hand2):
        cards = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
        hand1, hand2 = hand1[0], hand2[0]
        kind1 = hand_type(hand1)
        kind2 = hand_type(hand2)
        if kind1 < kind2:
            return -1
        if kind1 > kind2:
            return 1
        for card1, card2 in zip(hand1, hand2):
            if card1 == card2:
                continue
            if cards.index(card1) > cards.index(card2):
                return -1
            if cards.index(card1) < cards.index(card2):
                return 1
        return 0

    def hand_type(hand):
        values = list(Counter(list(hand)).values())
        if len(values) == 1:
            return 6
        if len(values) == 2 and 4 in values:
            return 5
        if len(values) == 2 and 3 in values:
            return 4
        if len(values) == 3 and 3 in values:
            return 3
        if len(values) == 3 and values.count(2) == 2:
            return 2
        if len(values) == 4:
            return 1
        return 0

    score = 0
    hands = sorted(data, key=cmp_to_key(compare))
    for i, hand in enumerate(hands):
        score += (i + 1) * hand[1]
    return score


def calc2(data):
    def compare(hand1, hand2):
        cards = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
        hand1, hand2 = hand1[0], hand2[0]
        kind1 = hand_type(hand1)
        kind2 = hand_type(hand2)
        if kind1 < kind2:
            return -1
        if kind1 > kind2:
            return 1
        for card1, card2 in zip(hand1, hand2):
            if card1 == card2:
                continue
            if cards.index(card1) > cards.index(card2):
                return -1
            if cards.index(card1) < cards.index(card2):
                return 1
        return 0

    def hand_type(hand):
        counts = Counter(list(hand))
        if len(counts) == 1:
            return 6
        if "J" in counts:
            j_count = counts.pop("J")
            keys = list(counts.keys())
            keys.sort(key=lambda x: counts[x])
            counts[keys[-1]] += j_count
        values = list(counts.values())
        if len(counts) == 1:
            return 6
        if len(values) == 2 and 4 in values:
            return 5
        if len(values) == 2 and 3 in values:
            return 4
        if len(values) == 3 and 3 in values:
            return 3
        if len(values) == 3 and values.count(2) == 2:
            return 2
        if len(values) == 4:
            return 1
        return 0

    score = 0
    hands = sorted(data, key=cmp_to_key(compare))
    for i, hand in enumerate(hands):
        score += (i + 1) * hand[1]
    return score


if testing:
    test_data_p = parse(test_data)

    if part1:
        res1 = calc(test_data_p)
        ans1 = test_ans1
        print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")
    if part2:
        res2 = calc2(test_data_p)
        ans2 = test_ans2
        print(f"Test part 2: {res2} ({ans2}){'   !!!' if res2 != ans2 else ''}")

if active:
    cookies = {"session": open("cookie.dat").read()}
    try:
        raw = open(f"{day}.txt").read()
    except FileNotFoundError:
        raw = requests.get(f"https://adventofcode.com/2023/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    data = parse(raw)
    if part1:
        print(f"Part 1: {calc(data)}")
    if part2:
        print(f"Part 2: {calc2(data)}")
