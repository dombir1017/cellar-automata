from VertData import ColoredTriangle
from math import sqrt
from pygame import Vector3
from random import randint
from typing import List, Dict

PHI = (1 + sqrt(5)) / 2
MAGIC_CONSTANT_1 = 2 / sqrt(10 + 2 * sqrt(5))  ## These come from normilzation of vector with 1, golden ratio and 0
MAGIC_CONSTANT_2 = (1 + sqrt(5)) / sqrt(10 + 2 * sqrt(5))

class Icosphere():
    icosahedron = [Vector3((-MAGIC_CONSTANT_1, MAGIC_CONSTANT_2, 0.0)),
                    Vector3((MAGIC_CONSTANT_1, MAGIC_CONSTANT_2, 0.0)),
                    Vector3((-MAGIC_CONSTANT_1, -MAGIC_CONSTANT_2, 0.0)),
                    Vector3((MAGIC_CONSTANT_1, -MAGIC_CONSTANT_2, 0.0)),
                    Vector3((0.0, -MAGIC_CONSTANT_1, MAGIC_CONSTANT_2)),
                    Vector3((0.0, MAGIC_CONSTANT_1, MAGIC_CONSTANT_2)),
                    Vector3((0.0, -MAGIC_CONSTANT_1, -MAGIC_CONSTANT_2)),
                    Vector3((0.0, MAGIC_CONSTANT_1, -MAGIC_CONSTANT_2)),
                    Vector3((MAGIC_CONSTANT_2, 0.0, -MAGIC_CONSTANT_1)),
                    Vector3((MAGIC_CONSTANT_2, 0.0, MAGIC_CONSTANT_1)),
                    Vector3((-MAGIC_CONSTANT_2, 0.0, -MAGIC_CONSTANT_1)),
                    Vector3((-MAGIC_CONSTANT_2, 0.0, MAGIC_CONSTANT_1))]
    icoindices = [
        [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
        [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
        [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
        [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]
    ]

    def __init__(self, depth):
        self.faces = []
        for i in range(20):
            self.subdivide(self.icosahedron[self.icoindices[i][0]],
                           self.icosahedron[self.icoindices[i][1]],
                           self.icosahedron[self.icoindices[i][2]], depth)            

    def subdivide(self, v1, v2, v3, depth):
        if depth == 0:
            ## make traingle between v1, v2, v3
            self.faces.append(CellularAutomotaTriangle(v1, v2, v3))
            return

        v12 = v1 + v2
        v23 = v2 + v3
        v31 = v3 + v1

        v12 = v12.normalize()
        v23 = v23.normalize()
        v31 = v31.normalize()

        self.subdivide(v1, v12, v31, depth - 1)
        self.subdivide(v2, v23, v12, depth - 1)
        self.subdivide(v3, v31, v23, depth - 1)
        self.subdivide(v12, v23, v31, depth - 1)

    def getVertNeighbours(self, v):
        faces: List[CellularAutomotaTriangle] = []
        for face in self.faces:
            if v in face._vertices:
                faces.append(face)
        return faces

    def calcNeighbours(self):
        # vtoface: Dict[str, List[CellularAutomotaTriangle]] = {}
        # for face in self.faces:
        #     for v in face._vertices:
        #         vtoface[str(v)] = self.getVertNeighbours(v)
        vtoface = {}
        for face in self.faces:
            for v in face._vertices:
                current = vtoface.get(str(v), [])
                vtoface[str(v)] = current + [face]


        for key in vtoface.keys():
            for face in vtoface[key]:
                face.neighbours.extend([e for e in vtoface[key] if e != face])

        for face in self.faces:
            face.neighbours = set(filter(lambda x: face.neighbours.count(x) == 2, face.neighbours))
           ## face.neighbours = dict(zip(face.neighbours, map(lambda x: face.neighbours.count(x), face.neighbours)))



    def tuple_to_string(self, x):
        return "(" + ", ".join(map(str, x)) + ")"


class CellularAutomotaTriangle(ColoredTriangle):
    def __init__(self, v1, v2, v3, color=(1, 0.5, 0)):
        super().__init__(v1, v2, v3, color)
        self.neighbours = []
        self.value = 0
    
    def showNeighbours(self):
        for n in self.neighbours:
            n.color = (1, 1, 1)

    def cal_next_value(self):
        n = sum(map(lambda p: p.value, self.neighbours))
        self.next_value = (not self.value, 0, 1, not self.value)[n]

    # def cal_next_value(self):
    #     n = sum(map(lambda p: p.value, self.neighbours))
    #     #self.next_value = max(-0.5 * (n - 1.5) ** 2 + 1, 0)
    #     self.next_value = max(2.3 * (2 ** -n) * (-0.75 * (n - 1.5) ** 2 + 1), 0)


    def change_to_next_value(self):
        self.value = self.next_value

    def update_color(self):
        self.color = (self.value, self.value, self.value)
    

