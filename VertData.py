from typing import Tuple, Iterable
from pygame import Vector3

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