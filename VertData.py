from typing import Tuple, Iterable
from pygame import Vector2, Vector3
from math import pi, sqrt
phi = (1 + 5 ** 0.5) / 2

class Mesh:
    def __init__(self):
        self._vertices: Iterable[Tuple[float, float, float]] = []
        self._edges: Iterable[Tuple[int, int]] = []

    def get_vert_data(self):
        output = []
        for edge in self._edges:
            for vertex in edge:
                output.append(self._vertices[vertex])
        return output
    
    def add_vertex(self, x: float, y: float, z: float) -> int:
        """Add's a vertex to the mesh
        Parameters: x, y,z The coordinates of the vertex
        Returns: The index of the vertex"""
        #print(x, y, z)
        self._vertices.append((x, y, z))
        return len(self._vertices) - 1
    
    def add_edge(self, i, j):
        self._edges.append((i, j))


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
        
class UVSphere(Mesh):
    icosahedron = list(map(lambda x: x.normalize(), map(Vector3, [
                    [-1,  phi,  0],
                    [ 1,  phi,  0],
                    [-1, -phi,  0],
                    [ 1, -phi,  0],
                    [ 0, -1,  phi],
                    [ 0,  1,  phi],
                    [ 0, -1, -phi],
                    [ 0,  1, -phi],
                    [ phi,  0, -1],
                    [ phi,  0,  1],
                    [-phi,  0, -1],
                    [-phi,  0,  1]])))
    
    icoindices = [
        [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
        [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
        [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
        [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]
    ]
    def __init__(self, depth):
        super().__init__()
        for i in range(20):
            self.subdivide(self.icosahedron[self.icoindices[i][0]],
                           self.icosahedron[self.icoindices[i][1]],
                           self.icosahedron[self.icoindices[i][2]], depth)

    def subdivide(self, v1, v2, v3, depth):
        if depth == 0:
            foo = self.add_vertex(*v1)
            bar = self.add_vertex(*v2)
            foobar = self.add_vertex(*v3)
            self.add_edge(foo, bar)
            self.add_edge(bar, foobar)
            self.add_edge(foobar, foo)
            return
        v12, v23, v31 = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]

        for i in range(3):
            v12[i] = v1[i] + v2[i]
            v23[i] = v2[i] + v3[i]
            v31[i] = v3[i] + v1[i]

        v12 = normalise(v12)
        v23 = normalise(v23)
        v31 = normalise(v31)
        self.subdivide(v1, v12, v31, depth - 1)
        self.subdivide(v2, v23, v12, depth - 1)
        self.subdivide(v3, v31, v23, depth - 1)
        self.subdivide(v12, v23, v31, depth - 1)


def normalise(v):
    d = sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
    v[0] /= d
    v[1] /= d
    v[2] /= d
    return v


