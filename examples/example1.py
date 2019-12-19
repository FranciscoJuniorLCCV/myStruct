# Example 1
import sys
import os

MYPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MYPATH + "/../")

from mystruct.material import Section
from mystruct.material import Material
from mystruct.element import Element
from mystruct.node import Node
from mystruct.solver import solve_eig

nodes_aux = [
    [0, 0],
    [2, 0],
    [2, 1.5],
    [4, 0]
]

elements_aux = [
    [0, 1, 0, 0],
    [0, 2, 0, 0],
    [1, 2, 0, 0],
    [2, 3, 0, 0],
    [1, 3, 0, 0]
]

constraints_aux = [
    [0, 1, 1],
    [3, 0, 1]
]

materials_aux = [
    {
        'type': 'steel',
        'young': 1e8,
        'rho': 2.714e3
    }
]

section_aux = [
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

aux_id_n = 0
node = []
for i in nodes_aux:
    node.append(Node(aux_id_n, i))
    aux_id_n += 1

aux_id_mat = 0
mat = []
for i in materials_aux:
    mat.append(Material(aux_id_mat, i['type'], i['young'], i['rho']))
    aux_id_mat += 1

aux_id_sec = 0
sec = []
for i in section_aux:
    sec.append(Section(aux_id_sec, i['type'], **i))
    aux_id_sec += 1

aux_id_e = 0
elem = []
for i in elements_aux:
    elem.append(Element(aux_id_e, node[i[0]], node[i[1]],
                        mat[i[2]].young, mat[i[2]].rho, sec[i[3]].area))
    aux_id_e += 1

solve_eig(elem, constraints_aux, node)

t = 1
# import json

# a = json.load(open('examples//teste.json'))
# ele = [tuple(a['elements'][i]) for i in range(len(a['elements']))]
