from Cells import CellularAutomotaTriangle
from typing import List
import math


class Projector:
    def __init__(self):
        self.face_to_vertex = {}

    # def construct_projection(self, s):  ## IDENITITY PROJECTION
    #     for f in s.faces:
    #         self.face_to_vertex[f] = f._vertices

    def construct_projection(self, s):
        self.face_to_vertex[s.faces[0]] = ((0, 0, 0), (0.2, 0, 0), (0.1, 0.1732, 0))
        to_process = list(zip(s.faces[0].neighbours, [(0, 0, 0), (0.2, 0, 0), (0.1, 0.1732, 0)], [(0.2, 0, 0), (0.1, 0.1732, 0), (0, 0, 0)], [(0.1, 0.1732, 0), (0, 0, 0), (0.2, 0, 0)]))
        print(to_process)
        while to_process != []:
           f, v1, v2, v3 = to_process.pop(0)
           if f in self.face_to_vertex.keys(): continue

           v_new = self.calc_final_vertices(v1, v2, v3)
           self.face_to_vertex[f] = (v1, v2, v_new)

           to_process.extend(list(zip(f.neighbours, (v1, v2, v_new), (v2, v_new, v1), (v_new, v2, v1))))
        print(f"number of projections: {len(self.face_to_vertex)}")
        print(f"Number of unique keys {len(set("".join(map(str, self.face_to_vertex.values()))))}")


    def calc_final_vertices(self, A, B, not_C):
        # Calculate the midpoint of A and B
        mid_x = (A[0] + B[0]) / 2
        mid_y = (A[1] + B[1]) / 2

        # Calculate the length of side AB
        side_length = math.sqrt((B[0] - A[0]) ** 2 + (B[1] - A[1]) ** 2)

        # Height of equilateral triangle using Pythagoras (height = sqrt(3) / 2 * side_length)
        height = math.sqrt(3) / 2 * side_length

        # Slope of line perpendicular to AB
        dx = B[0] - A[0]
        dy = B[1] - A[1]

        # The perpendicular slope (negative reciprocal)
        perp_slope_x = -dy
        perp_slope_y = dx

        # Normalize the perpendicular vector
        perp_length = math.sqrt(perp_slope_x ** 2 + perp_slope_y ** 2)
        unit_perp_x = perp_slope_x / perp_length
        unit_perp_y = perp_slope_y / perp_length

        # Two possible positions for the third vertex (above or below the line AB)
        C1 = (mid_x + height * unit_perp_x, mid_y + height * unit_perp_y, 0)
        C2 = (mid_x - height * unit_perp_x, mid_y - height * unit_perp_y, 0)
        print(C1, C2, not_C)
        if self.distance(C1, not_C) > 0.0001 and self.distance(C2, not_C) > 0.0001: input()
        return C2 if self.distance(C1, not_C) > 0.0001 else C1  # Return both possibilities for the third vertex
    
    def distance(self, A, B):
        return ((A[0] - B[0]) ** 2) - ((A[1] - B[1]) ** 2)

    def get_verticies(self, f):
        return self.face_to_vertex[f]