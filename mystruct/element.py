import numpy as np
from scipy.sparse import coo_matrix


class Element:
    """Class with the definition of the element
    """

    def __init__(self, _id, node1, node2, young, area, rho):
        self.id = _id
        self.node1 = node1
        self.node2 = node2
        self.young = young
        self.rho = rho
        self.area = area
        self.length = None
        self.constitutive_matrix = None
        self.rotation_matrix = None
        self.stiffness_matrix = None
        self.mass_matrix = None
        self.traction = None
        self.calc_length()
        self.compile_rotation_matrix()
        self.compile_constitutive_matrix()
        self.compile_stiffness_matrix()
        self.compile_mass_matrix()

    def calc_length(self):
        self.length = length_element_plane(self.node1, self.node2)

    def compile_rotation_matrix(self):
        self.rotation_matrix = rot_mat_plane_truss(self.node1, self.node2)

    def compile_constitutive_matrix(self):
        self.constitutive_matrix = const_mat_plane_truss(self.young,
                                                         self.area, self.length)

    def compile_stiffness_matrix(self):
        self.stiffness_matrix = stiffness_matrix(self.constitutive_matrix,
                                                 self.rotation_matrix)

    def compile_mass_matrix(self):
        self.mass_matrix = conc_mass_mat_plane_truss(self.area, self.length,
                                                     self.rho)


def const_mat_plane_truss(E_ele, A_ele, L):
    """Constitutive matrix of a Truss element

    Args:
        E_ele (float): Young modulus of the element
        A_ele (float): Area of the element
        L (float): Length of the element

    Returns:
        array: Constitutive matrix
    """
    EA = E_ele * A_ele
    matrix = EA / L * np.array(
        [
            [1.0, 0.0, -1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [-1.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0]
        ]
    )
    return matrix


def const_mat_plane_beam(E_ele, I_ele, L):
    """Constitutive matrix of a Beam element

    Args:
        E_ele (float): Young modulus of the element
        I_ele (float): Moment of the Inertia of the element
        L (float): Length of the element

    Returns:
        array: Constitutive matrix
    """
    EI = E_ele * I_ele
    a = 12.0 / (L * L)
    b = 6.0 / L
    matrix = EI / L * np.array(
        [
            [a, b, -a, b],
            [b, 4.0, -b, 2.0],
            [-a, -b, a, -b],
            [b, 2.0, -b, 4.0]
        ]
    )
    return matrix


def const_mat_plane_frame(E_ele, A_ele, I_ele, L):
    """Constitutive matrix of a Frame element

    Args:
        E_ele (float): Young modulus of the element
        A_ele (float): Area of the element
        I_ele (float): Moment of the Inertia of the element
        L (float): Length of the element

    Returns:
        array: Constitutive matrix
    """
    a = 12.0 * E_ele * I_ele / (L * L * L)
    b = 6 * E_ele * I_ele / (L * L)
    c = 2.0 * E_ele * I_ele / L
    d = E_ele * A_ele / L
    matrix = np.array(
        [
            [d, 0.0, 0.0, -d, 0.0, 0.0],
            [0.0, a, b, 0.0, -a, b],
            [0.0, b, 2.0 * c, 0.0, -b, c],
            [-d, 0.0, 0.0, d, 0.0, 0.0],
            [0.0, -a, -b, 0.0, a, -b],
            [0.0, b, c, 0.0, -b, 2.0 * c],
        ]
    )
    return matrix


def length_element_plane(node1, node2):
    """Length of the element in 2D

    Args:
        node1 (array): First node of the element
        node2 (array): Second node of the element

    Returns:
        float: Length of the element
    """
    xa = node2[0] - node1[0]
    ya = node2[1] - node1[1]
    return np.sqrt(xa * xa + ya * ya)


def length_element_space(node1, node2):
    """Length of the element in 3D

    Args:
        node1 (array): First node of the element
        node2 (array): Second node of the element

    Returns:
        float: Length of the element
    """
    xa = node2[0] - node1[0]
    ya = node2[1] - node1[1]
    za = node2[2] - node1[2]
    return np.sqrt(xa * xa + ya * ya + za * za)


def rot_mat_plane_truss(node1, node2):
    """Rotation matrix for 2D structure

    Args:
        node1 (array): First node of the element
        node2 (array): Second node of the element

    Returns:
        array: Rotation matrix
    """
    xa = node2[0] - node1[0]
    ya = node2[1] - node1[1]
    L = np.sqrt(xa * xa + ya * ya)
    cos = xa / L
    sin = ya / L
    r = np.array(2*[cos, sin, -sin, cos])

    row = np.array(np.sort(2*list(range(0, 4))))
    col = np.concatenate([2*[i, i+1] for i in range(0, 4, 2)])

    rotate = coo_matrix((r, (row, col)), shape=(4, 4)).toarray()

    return rotate


def rot_mat_plane_frame(node1, node2):
    """Rotation matrix for 2D structure

    Args:
        node1 (array): First node of the element
        node2 (array): Second node of the element

    Returns:
        array: Rotation matrix
    """
    xa = node2[0] - node1[0]
    ya = node2[1] - node1[1]
    L = np.sqrt(xa * xa + ya * ya)
    cos = xa / L
    sin = ya / L
    r = np.array(2 * [cos, sin, -sin, cos])

    row = np.array(np.sort(2 * [0, 1, 3, 4]))
    col = np.concatenate([2*[i, i+1] for i in range(0, 5, 3)])

    rotate = coo_matrix((r, (row, col)), shape=(6, 6)).toarray()
    rotate[2][2] = rotate[5][5] = 1

    return rotate


def rot_mat_space_truss(node1, node2):
    """Rotation matrix for 3D structure

    Args:
        node1 (array): First node of the element
        node2 (array): Second node of the element

    Returns:
        array: Rotation matrix
    """
    xa = node2[0] - node1[0]
    ya = node2[1] - node1[1]
    za = node2[2] - node1[2]
    L = np.sqrt(xa * xa + ya * ya + za * za)
    cxx = xa / L
    cyx = ya / L
    czx = za / L
    d = np.sqrt(cxx * cxx + cyx * cyx)
    cxy = -cyx / d
    cyy = cxx / d
    czy = 0
    cxz = -cxx * czx / d
    cyz = -cyx * czx / d
    czz = d
    var_lambda = np.array(4*[cxx, cyx, czx, cxy, cyy, czy, cxz, cyz, czz])

    row = np.array(np.sort(3*list(range(0, 12))))
    col = np.concatenate([3*[i, i+1, i+2] for i in range(0, 12, 3)])

    rotate = coo_matrix((var_lambda, (row, col)), shape=(12, 12)).toarray()

    return rotate


def stiffness_matrix(constitutive, rotation):
    """Stiffness matrix of the element

    Args:
        constitutive (array): Constitutive matrix
        rotation (array): Rotation matrix

    Returns:
        array: Stiffness Matrix
    """
    return np.dot(np.dot(np.transpose(rotation), constitutive), rotation)


def conc_mass_mat_plane_truss(area, L, rho):
    """Concentrate Mass matrix for a 2D truss

    Args:
        area (float): Area of the element
        L (float): Length of the element
        rho (float): Poisson ratio of the material

    Returns:
        array: Mass matrix
    """
    return (rho * area * L / 2.0) * np.eye(4)


def conc_mass_mat_space_truss(area, L, rho):
    """Concentrate Mass matrix for a 3D truss

    Args:
        area (float): Area of the element
        L (float): Length of the element
        rho (float): Poisson ratio of the material

    Returns:
        array: Mass matrix
    """
    return (rho * area * L / 2.0) * np.eye(6)
