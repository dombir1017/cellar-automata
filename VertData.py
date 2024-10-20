from typing import Tuple, Iterable, List, Dict
from pygame import Vector3
from math import sqrt

PHI = (1 + sqrt(5)) / 2
MAGIC_CONSTANT_1 = 2 / sqrt(10 + 2 * sqrt(5))  ## These come from normilzation of vector with 1, golden ratio and 0
MAGIC_CONSTANT_2 = (1 + sqrt(5)) / sqrt(10 + 2 * sqrt(5))

class Mesh:
    def __init__(self, *arg):
        self._vertices: Iterable[Tuple[float, float, float]] = []
        for v in arg:
            self.add_vertex(*v)

    def get_vert_data(self):
        """Get the mesh vertex data in order"""
        return self._vertices
    
    def add_vertex(self, x: float, y: float, z: float) -> int:
        """Add's a vertex to the mesh
        Parameters: x, y,z The coordinates of the vertex
        Returns: The index of the vertex"""
        self._vertices.append((x, y, z))
        return len(self._vertices) - 1

class ColoredTriangle(Mesh):
    def __init__(self, v1, v2, v3, color = (1, 0.5, 0)):
        super().__init__(v1, v2, v3)
        self.color = color

    def change_color(self, r, g, b):
        self.color = (r, g, b)
        
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
        self.faces.append(ColoredTriangle(v1, v2, v3))


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