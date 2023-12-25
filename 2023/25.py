import networkx
import requests

day = 25
part1 = True
testing = True
active = True

test_data = """
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""

test_ans1 = 54


def parse(indata):
    data_rows = indata.split("\n")
    data = []
    for row in data_rows:
        if not row:
            continue
        ps = row.split(":")
        data.extend((ps[0], n2) for n2 in ps[1].split())
    return data


def calc(data):
    graph = networkx.Graph()
    graph.add_edges_from(data)

    to_cut = networkx.minimum_edge_cut(graph)
    if len(to_cut) != 3:
        print("Can't split with three cuts")
    for c in to_cut:
        graph.remove_edge(c[0], c[1])

    score = 1
    for group in networkx.connected_components(graph):
        score *= len(group)
    return score


if testing:
    if part1:
        test_data_p = parse(test_data)
        res1 = calc(test_data_p)
        ans1 = test_ans1
        print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")

if active:
    cookies = {"session": open("cookie.dat").read()}
    try:
        raw = open(f"{day}.txt").read()
    except FileNotFoundError:
        raw = requests.get(f"https://adventofcode.com/2023/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    if part1:
        data = parse(raw)
        print(f"Part 1: {calc(data)}")
