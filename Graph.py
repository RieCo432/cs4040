import matplotlib.pyplot as plt
import numpy as np
from Edge import Edge
from Vertex import Vertex
import pickle


class Graph:

    def __init__(self, width, height):
        self.vertices = np.ndarray((width, height), dtype='object')
        self.edges = []
        self.start = (0, 0)
        self.start_index = 0
        self.end = (width-1, height-1)
        self.end_index = (width-1) * width + (height-1)

    def set_start(self, x, y):
        self.start = (x, y)
        self.start_index = x * self.vertices.shape[0] + y

    def set_end(self, x, y):
        self.end = (x, y)
        self.end_index = x * self.vertices.shape[0] + y

    def add_vertex(self, x, y):
        self.vertices[x, y] = Vertex(x * self.vertices.shape[0] + y)

    def add_edge(self, from_x, from_y, to_x, to_y, weight):
        if to_x < 0 or from_x < 0 or to_y < 0 or from_y < 0:
            print("Point outside of map")
            return
        if abs(to_x - from_x) + abs(to_y - from_y) > 1:
            print("Cannot connect nodes further than 1 apart")
            return
        new_edge = Edge(self.vertices[from_x, from_y], self.vertices[to_x, to_y], weight)
        self.edges.append(new_edge)
        if to_x > from_x:
            self.vertices[from_x, from_y].east = new_edge
        elif to_x < from_x:
            self.vertices[from_x, from_y].west = new_edge
        elif to_y > from_y:
            self.vertices[from_x, from_y].south = new_edge
        elif to_y < from_y:
            self.vertices[from_x, from_y].north = new_edge

        self.vertices[from_x, from_y].update_edges()

    def get_vertex_coordinates(self, vertex):
        y = vertex.pos % self.vertices.shape[0]
        x = (vertex.pos - y) // self.vertices.shape[0]
        return (x, y)

    def show_graph(self, path=None):
        width = 4 * self.vertices.shape[0] - 2
        height = 4 * self.vertices.shape[1] - 2
        image = np.zeros((width, height, 3), dtype=int)

        for x in range(self.vertices.shape[0]):
            for y in range(self.vertices.shape[1]):
                if path is None or self.vertices[x, y] not in path:
                    color = self.vertices[x, y].color
                elif path is not None and self.vertices[x, y] in path:
                    color = (0, 0, 255)

                image[4 * x, 4 * y] = color
                image[4 * x, 4 * y + 1] = color
                image[4 * x + 1, 4 * y] = color
                image[4 * x + 1, 4 * y + 1] = color

                north_color = (0, 0, 0)
                east_color = (0, 0, 0)
                south_color = (0, 0, 0)
                west_color = (0, 0, 0)

                if self.vertices[x, y].north is not None:
                    north_color = self.vertices[x, y].north.get_color()
                if self.vertices[x, y].east is not None:
                    east_color = self.vertices[x, y].east.get_color()
                if self.vertices[x, y].south is not None:
                    south_color = self.vertices[x, y].south.get_color()
                if self.vertices[x, y].west is not None:
                    west_color = self.vertices[x, y].west.get_color()

                if 4 * y - 1 > 0:
                    image[4 * x, 4 * y - 1] = north_color
                    image[4 * x, 4 * y - 2] = north_color

                if 4 * x + 2 < image.shape[0]:
                    image[4 * x + 2, 4 * y] = east_color
                    image[4 * x + 3, 4 * y] = east_color

                if 4 * y + 2 < image.shape[1]:
                    image[4 * x + 1, 4 * y + 2] = south_color
                    image[4 * x + 1, 4 * y + 3] = south_color

                if 4 * x - 1 > 0:
                    image[4 * x - 1, 4 * y + 1] = west_color
                    image[4 * x - 2, 4 * y + 1] = west_color

        if path is not None:
            color = (0, 0, 255)
            for i in range(len(path)-1):
                x, y = self.get_vertex_coordinates(path[i])
                if path[i].north is not None and path[i].north.to_vertex == path[i+1]:
                    image[4 * x, 4 * y - 1] = color
                    image[4 * x, 4 * y - 2] = color
                elif path[i].east is not None and path[i].east.to_vertex == path[i+1]:
                    image[4 * x + 2, 4 * y] = color
                    image[4 * x + 3, 4 * y] = color
                elif path[i].south is not None and path[i].south.to_vertex == path[i+1]:
                    image[4 * x + 1, 4 * y + 2] = color
                    image[4 * x + 1, 4 * y + 3] = color
                elif path[i].west is not None and path[i].west.to_vertex == path[i+1]:
                    image[4 * x - 1, 4 * y + 1] = color
                    image[4 * x - 2, 4 * y + 1] = color

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
