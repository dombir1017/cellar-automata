from typing import Tuple, Iterable
from pygame import Vector2, Vector3

class Mesh:
    def __init__(self):
        self._vertices: Iterable[Tuple[float, float, float]] = ()
        self._edges: Iterable[Tuple[int, int]] = ()

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
        self._vertices.append((x, y, z))
        return len(self._vertices)


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
    def __init__(self, n_slices, n_stacks):
        super.__init__()
        self.add_vertex(0, 1, 0)

        for i in range(n_stacks):
            pass
