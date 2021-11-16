class Edge:

    def __init__(self, from_node, to_node, weight):
        self.from_node = from_node
        self.to_note = to_node
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
