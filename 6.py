#!/usr/bin/env python3

import sys

class Node:
    def __init__(self, name, parent = None):
        self.name = name
        self.children = []
        self.parent = parent

    def find_child(self, name):
        if self.name == name:
            return self
        for child in self.children:
            result = child.find_child(name)
            if result:
                return result
        return None

    def parents(self,):
        if self.parent == None:
            return [self.name]
        return [self.name] + self.parent.parents()

    def nr_parents(self):
        if self.parent == None:
            return 0
        return self.parent.nr_parents() + 1

    def nr_orbits(self):
        amount = self.nr_parents()
        for child in self.children:
            amount += child.nr_orbits()
        return amount

    def print_children(self, indent=0):
        ind = indent * ' '
        print(f'{ind}Node: {self.name}')
        for child in self.children:
            child.print_children(indent+1)
        

def add_connections(node):
    if node.name in connections:
        children = connections[node.name]
        for child in children:
            current = Node(child, node)
            add_connections(current)
            node.children.append(current)
            

if __name__ == '__main__':
    root = None
    with open(sys.argv[1]) as infile:
        connections = dict()
        for line in infile:
            parent, child = line.strip().split(')')
            if parent in connections:
                connections[parent].append(child)
            else:
                connections[parent] = [child]

        root = Node('COM')
        add_connections(root)

    print(f'Part a: {root.nr_orbits()}')

    node1_parents = root.find_child('YOU').parents()
    node2_parents = root.find_child('SAN').parents()
    i = -1
    while node1_parents[i] == node2_parents[i]:
        i -= 1

    dist = len(node1_parents) + len(node2_parents) + 2*i
    print(f'Part b: {dist}')
