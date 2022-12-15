import requests

day = 7


class Folder:
    def __init__(self, parent):
        self._parent = parent
        self._files = {}
        self._dirs = {}

    def parent(self):
        return self._parent

    def add_file(self, filename, size):
        if size is None:
            self._dirs[filename] = Folder(self)
        else:
            self._files[filename] = size

    def enter(self, filename):
        return self._dirs[filename]

    def size(self):
        size = sum(self._files.values())
        for folder in self._dirs:
            size += self._dirs[folder].size()
        return size

    def folder_sizes(self):
        sizes = []
        sizes.append(sum(self._files.values()))
        for folder in self._dirs:
            f_sizes = self._dirs[folder].folder_sizes()
            sizes[0] += f_sizes[0]
            sizes += f_sizes
        return sizes

    def print(self):
        print("Folders:")
        for folder in self._dirs:
            print(f"{folder}:")
            self._dirs[folder].print()
        print("Files:")
        for entry in self._files:
            print(f"{entry}: {self._files[entry]}")


def calc(data):
    score = 0

    root = Folder(None)
    pwd = root

    for row in data:
        if row[0] == "$":
            if row.startswith("$ ls"):
                continue
            elif row.startswith("$ cd"):
                parts = row.split()
                if parts[2] == "/":
                    pwd = root
                elif parts[2] == "..":
                    pwd = pwd.parent()
                else:
                    pwd = pwd.enter(parts[2])
        else:
            parts = row.split()
            if parts[0] == "dir":
                pwd.add_file(parts[1], None)
            else:
                pwd.add_file(parts[1], int(parts[0]))

    sizes = [size for size in root.folder_sizes() if size < 100000]

    score = sum(sizes)
    return score


def calc2(data):
    score = 0

    root = Folder(None)
    pwd = root

    for row in data:
        if row[0] == "$":
            if row.startswith("$ ls"):
                continue
            elif row.startswith("$ cd"):
                parts = row.split()
                if parts[2] == "/":
                    pwd = root
                elif parts[2] == "..":
                    pwd = pwd.parent()
                else:
                    pwd = pwd.enter(parts[2])
        else:
            parts = row.split()
            if parts[0] == "dir":
                pwd.add_file(parts[1], None)
            else:
                pwd.add_file(parts[1], int(parts[0]))

    total = 70000000
    sizes = root.folder_sizes()
    needed = 30000000 - (total - sizes[0])
    sizes.sort()
    for val in sizes:
        if val > needed:
            return val
    return score


test_data = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""
test_data = [row for row in test_data.split("\n") if row]


res1 = calc(test_data)
res2 = calc2(test_data)
ans1 = 95437
ans2 = 24933642
print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")
print(f"Test part 2: {res2} ({ans2}){'   !!!' if res2 != ans2 else ''}")

cookies = {"session": open("cookie.dat").read()}
req = requests.get(f"https://adventofcode.com/2022/day/{day}/input", cookies=cookies)
data = req.text.split("\n")
data = [row for row in data if row]

print(f"Part 1: {calc(data)}")
print(f"Part 2: {calc2(data)}")
