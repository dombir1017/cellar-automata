from typing import Tuple

class Shape:
    def __init__(self):
        self.vertices: Tuple[Tuple[float, float, float]] = ()
        self.edges: Tuple[Tuple[int, int]] = ()

    def get_vert_data(self):
        output = []
        for edge in self.edges:
            for vertex in edge:
                output.append(self.vertices[vertex])
        return output


class Cube(Shape): 
    def __init__(self):
        self.vertices = (
            (1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1),
            (-1, -1, -1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, -1, 1),
            (-1, 1, 1)
            )

        self.edges = (
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