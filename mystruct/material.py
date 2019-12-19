import numpy as np

class Material:
    def __init__(self, id, type, young, rho):
        self.id = id
        self.type = type
        self.young = young
        self.rho = rho

class Section:
    def __init__(self, id, typeSec, **kwargs):
        self.id = id
        self.typeSec = typeSec
        self.kwargs = kwargs
        self.area = self.compute_area()

    def compute_area(self):
        if self.typeSec == 'square':
            area = self.kwargs.get('sideLen') * self.kwargs.get('sideLen')
            return area
        elif self.typeSec == 'rectangle':
            area = self.kwargs.get('sideLen') * self.kwargs.get('width')
            return area
        elif self.typeSec == 'circle':
            area = np.pi * self.kwargs.get('radius') * self.kwargs.get('radius')
            return area
        elif self.typeSec == 'ring':
            area = np.pi * self.kwargs.get('outRadius') * \
                self.kwargs.get('outRadius') - np.pi * \
                self.kwargs.get('innerRadius') * self.kwargs.get('innerRadius')
            return area
