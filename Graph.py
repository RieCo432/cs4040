import matplotlib.pyplot as plt
import numpy as np


class Graph:

    def __init__(self, width, height):
        self.nodes = np.zeros((width, height))
        self.edges = []
        self.start = (0, 0)
        self.end = (width-1, height-1)

    def __int__(self):
        return 255

    def set_start(self, x, y):
        self.start = (x, y)

    def set_end(self, x, y):
        self.end = (x, y)

    def show_graph(self):
        width = 4 * self.nodes.shape[0] - 2
        height = 4 * self.nodes.shape[1] - 2
        graph = np.zeros((width, height))

        for x in range(self.nodes.shape[0]):
            for y in range(self.nodes.shape[1]):
                graph[4*x, 4*y] = int(self.nodes[x, y])
                graph[4*x, 4*y+1] = int(self.nodes[x, y])
                graph[4*x+1, 4*y] = int(self.nodes[x, y])
                graph[4*x+1, 4*y+1] = int(self.nodes[x, y])

        plt.imshow(graph, cmap='gray')
        plt.show()