from VertData import ColoredTriangle, Icosphere

class CellularAutomotaTriangle(ColoredTriangle):
    def __init__(self, v1, v2, v3, color=(1, 0.5, 0)):
        super().__init__(v1, v2, v3, color)
        self.neighbours = []
        self.value, self.next_value = 0, 0
    
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

class IcosphereCellularAutomate(Icosphere):
    def __init__(self, depth):
        super().__init__(depth)
    
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

    def make_face(self, v1, v2, v3):
        return self.faces.append(CellularAutomotaTriangle(v1, v2, v3))
    
    def update_color(self):
        for f in self.faces:
            f.recalc_color_from_value()