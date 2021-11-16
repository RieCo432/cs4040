class Node:

    def __init__(self):
        self.north = None
        self.east = None
        self.south = None
        self.west = None

    def get_edges(self):
        return [edge for edge in [self.north, self.east, self.south, self.west] if edge is not None]

    @staticmethod
    def get_color():
        return [255, 255, 255]
