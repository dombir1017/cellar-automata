from typing import Tuple, Iterable, List, Dict
from pygame import Vector3
from math import sqrt

PHI = (1 + sqrt(5)) / 2
MAGIC_CONSTANT_1 = 2 / sqrt(10 + 2 * sqrt(5))  ## These come from normilzation of vector with 1, golden ratio and 0
MAGIC_CONSTANT_2 = (1 + sqrt(5)) / sqrt(10 + 2 * sqrt(5))

class Mesh:
    def __init__(self, *arg):
        self._vertices: List[Vector3] = list(arg)


    def get_vert_data(self):
        """Get the mesh vertex data in order"""
        return self._vertices
    
    def add_vertex(self, p : Vector3) -> int:
        """Add's a vertex to the mesh
        Parameters: x, y,z The coordinates of the vertex
        Returns: The index of the vertex"""
        self._vertices.append(p)
        return len(self._vertices) - 1

class CellularAutomotaTriangle(Mesh):
    def __init__(self, v1, v2, v3, color=(1, 0.5, 0)):
        super().__init__(v1, v2, v3)
        self.color = color
        self.neighbours = []
        self.value, self.next_value = 0, 0
    
    def change_color(self, r, g, b):
        self.color = (r, g, b)

    def showNeighbours(self):
        for n in self.neighbours:
            n.color = (1, 1, 1)

    def cal_next_value(self):
        n = sum(map(lambda p: p.value, self.neighbours))
        self.next_value = (not self.value, 0, 1, not self.value)[n]

    def change_to_next_value(self):
        self.value = self.next_value

    def recalc_color_from_value(self):
        self.change_color(self.value, self.value, self.value)
        
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
            self.make_face(v1, v2, v3)
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

    def make_face(self, v1, v2, v3):
       self.faces.append(CellularAutomotaTriangle(v1, v2, v3))

    def calcNeighbours(self):
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

    def update_color(self):
        for f in self.faces:
            f.recalc_color_from_value()


class Cube(Mesh): 
   def __init__(self):
       self._vertices = (
           (1, -1, -1),
           (1, 1, -1),
           (-1, 1, -1),
           (-1, -1, -1),
           (1, -1, 1),
           (1, 1, 1),
           (-1, -1, 1),
           (-1, 1, 1)
           )

       self._edges = (
           (0,1),
           (0,3),
           (0,4),
           (2,1),
           (2,3),
           (2,7),
           (6,3),
           (6,4),
           (6,7),
           (5,1),
           (5,4),
           (5,7)
           )