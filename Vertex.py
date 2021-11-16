class Vertex:

    def __init__(self, pos):
        self.north = None
        self.east = None
        self.south = None
        self.west = None
        self.edges = []
        self.pos = pos
        self.color = (255, 255, 255)

    def update_edges(self):
        self.edges = [edge for edge in [self.north, self.east, self.south, self.west] if edge is not None]

    def get_weight_to(self, to_vertex):
        for edge in self.edges:
            if edge.to_vertex == to_vertex:
                return edge.weight
