#!/usr/bin/env python3

import sys

def split_to_layers(data, height, width):
    layers = []
    layer_size = height*width
    for i in range(0, len(data), layer_size):
        layers.append(data[i:i+layer_size])
    return layers

HEIGHT=6
WIDTH=25

with open(sys.argv[1]) as infile:
    data = infile.read().strip()

layers = split_to_layers(data, HEIGHT, WIDTH)
best = 0
best_zeroes = float('inf')
for i, layer in enumerate(layers):
    if (count := layer.count('0')) < best_zeroes:
        best = i
        best_zeroes = count

print(f'Part a: {layers[best].count("1")*layers[best].count("2")}')

image = ['2']*WIDTH*HEIGHT

for layer in layers:
    for i, color in enumerate(layer):
        if image[i] == '2':
            image[i] = color

print('Part b:')
image = ''.join(image)
image = image.replace('2', ' ')
image = image.replace('0', ' ')
for i in range(0, len(image), WIDTH):
    print(image[i:i+WIDTH])
