class Edge:

    def __init__(self, from_vertex, to_vertex, weight):
        self.from_vertex = from_vertex
        self.to_vertex = to_vertex
        self.weight = weight

    def get_color(self):
        red = 0
        green = 0
        if self.weight < 128:
            green = 255
            red = 2 * self.weight
        elif self.weight >= 128:
            red = 255
            green = 255 - 2 * (self.weight - 128)

        return [red, green, 0]
