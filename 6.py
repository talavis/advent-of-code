#!/usr/bin/env python3

import sys

class Node:
    def __init__(self, name, parent = None):
        self.name = name
        self.children = []
        self.parent = parent

    def find(self, name):
        if self.name == name:
            return self
        for child in self.children:
            result = child.find(name)
            if result:
                return result
        return None

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
        

if __name__ == '__main__':
    root = None
    with open(sys.argv[1]) as infile:
        for line in infile:
            parent, child = line.strip().split(')')

            if parent == 'COM':
                root = Node(parent)
                current = root
            else:
                current = root.find(parent)

            current.children.append(Node(child, current))

    print(f'Part a: {root.nr_orbits()}')
        
