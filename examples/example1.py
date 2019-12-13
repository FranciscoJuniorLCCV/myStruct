# Example 1
nodes = [
    [0, 0],
    [2, 0],
    [2, 1.5],
    [4, 0]
]

elements = [
    [0, 1, 0, 0],
    [0, 2, 0, 0],
    [1, 2, 0, 0],
    [2, 3, 0, 0],
    [1, 4, 0, 0]
]

constraints = [
    [0, 1, 1],
    [3, 0, 1]
]

materials = [
    {
        'type': 'steel',
        'young': 1e8,
        'rho': 2.714e3
    }
]

section = [
    {
        'type': 'square',
        'sideLen': 0.2
    },
    {
        'type': 'rectangle',
        'sideLen': 10,
        'width': 4
    },
    {
        'type': 'circle',
        'radius': 10
    },
    {
        'type': 'ring',
        'outRadius': 10,
        'innerRadius': 8
    }
]

# import json

# a = json.load(open('examples//teste.json'))
# ele = [tuple(a['elements'][i]) for i in range(len(a['elements']))]
# t = 1