import matplotlib.pyplot as plt
import numpy as np
from Edge import Edge
from Node import Node
import pickle


class Graph:

    def __init__(self, width, height):
        self.nodes = np.ndarray((width, height), dtype='object')
        self.edges = []
        self.start = (0, 0)
        self.end = (width-1, height-1)

    def set_start(self, x, y):
        self.start = (x, y)

    def set_end(self, x, y):
        self.end = (x, y)

    def add_node(self, x, y):
        self.nodes[x, y] = Node()

    def add_edge(self, from_x, from_y, to_x, to_y, weight):
        if to_x < 0 or from_x < 0 or to_y < 0 or from_y < 0:
            print("Point outside of map")
            return
        if abs(to_x - from_x) + abs(to_y - from_y) > 1:
            print("Cannot connect nodes further than 1 apart")
            return
        new_edge = Edge(self.nodes[from_x, from_y], self.nodes[to_x, to_y], weight)
        self.edges.append(new_edge)
        if to_x > from_x:
            self.nodes[from_x, from_y].east = new_edge
        elif to_x < from_x:
            self.nodes[from_x, from_y].west = new_edge
        elif to_y > from_y:
            self.nodes[from_x, from_y].south = new_edge
        elif to_y < from_y:
            self.nodes[from_x, from_y].north = new_edge

    def show_graph(self):
        width = 4 * self.nodes.shape[0] - 2
        height = 4 * self.nodes.shape[1] - 2
        image = np.zeros((width, height, 3), dtype=int)

        for x in range(self.nodes.shape[0]):
            for y in range(self.nodes.shape[1]):
                image[4*x, 4*y] = self.nodes[x, y].get_color()
                image[4*x, 4*y+1] = self.nodes[x, y].get_color()
                image[4*x+1, 4*y] = self.nodes[x, y].get_color()
                image[4*x+1, 4*y+1] = self.nodes[x, y].get_color()

                north_value = 0
                east_value = 0
                south_value = 0
                west_value = 0

                if self.nodes[x, y].north is not None:
                    north_value = self.nodes[x, y].north.get_color()
                if self.nodes[x, y].east is not None:
                    east_value = self.nodes[x, y].east.get_color()
                if self.nodes[x, y].south is not None:
                    south_value = self.nodes[x, y].south.get_color()
                if self.nodes[x, y].west is not None:
                    west_value = self.nodes[x, y].west.get_color()

                if 4 * y - 1 > 0:
                    image[4 * x, 4 * y - 1] = north_value
                    image[4 * x, 4 * y - 2] = north_value

                if 4 * x + 2 < image.shape[0]:
                    image[4 * x + 2, 4 * y] = east_value
                    image[4 * x + 3, 4 * y] = east_value

                if 4 * y + 2 < image.shape[1]:
                    image[4 * x + 1, 4 * y + 2] = south_value
                    image[4 * x + 1, 4 * y + 3] = south_value

                if 4 * x - 1 > 0:
                    image[4 * x - 1, 4 * y + 1] = west_value
                    image[4 * x - 2, 4 * y + 1] = west_value

        image = np.flip(np.rot90(image, k=3, axes=(0, 1)), axis=1)
        plt.imshow(image)
        plt.show()

    @staticmethod
    def save_graph(graph, filename):
        with open("graphs/"+filename+".pickle", "wb") as outfile:
            pickle.dump(graph, outfile)

    @staticmethod
    def load_graph(filename):
        with open("graphs/"+filename+".pickle", "rb") as infile:
            return pickle.load(infile)
