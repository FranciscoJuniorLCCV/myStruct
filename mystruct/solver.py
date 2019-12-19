import numpy as np
from scipy import linalg

def global_stiff_mass(elem, constraints_aux, node):
    glibn = len(node) * len(node[0].coords) * [0]
    nglib = 0

    for i in constraints_aux:
        for j in range(len(i) - 1):
            if i[j + 1] == 1:
                glibn[(len(i) - 1) * i[0] + j] = -1

    for i in range(len(glibn)):
        if glibn[i] == 0:
            glibn[i] = nglib
            nglib += 1

    kg = np.zeros((nglib, nglib))
    mg = np.zeros((nglib, nglib))

    for i in elem:
        glibe = [glibn[i.node1.id * 2], glibn[i.node1.id * 2 + 1],
                 glibn[i.node2.id * 2], glibn[i.node2.id * 2 + 1]]
        for j in range(len(glibe)):
            if glibe[j] != -1:
                for k in range(len(glibe)):
                    if glibe[k] != -1:
                        kg[glibe[j]][glibe[k]] += i.stiffness_matrix[j][k]
                        mg[glibe[j]][glibe[k]] += i.mass_matrix[j][k]

    return kg, mg

def solve_eig(elem, constraints_aux, node):
    kg, mg = global_stiff_mass(elem, constraints_aux, node)
    d, v = linalg.eig(kg, b=mg)
    print(d)
    print(v)
