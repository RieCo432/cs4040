from Graph import Graph
from algorithms import Dijkstra
from random import random, randint
import numpy as np


def generate_graph(width, height, hard_obstacles_density=0.0, soft_obstacles_density=0.0): #, soft_obstacle_min=0, soft_obstacle_max=255, distribution="equal"):

    g = None
    path = []

    def generate_weight():
        if random() < soft_obstacles_density:
            return np.random.normal(loc=128, scale=16)
        else:
            return 10

    while len(path) == 0:

        g = Graph(width, height)

        g.set_start(randint(0, width // 2), randint(0, height // 2))
        g.set_end(randint(width // 2, width - 1), randint(height // 2, height - 1))

        for x in range(width):
            for y in range(height):
                g.add_vertex(x, y)

        for x in range(width):
            for y in range(height):
                if x > 0:
                    g.add_edge(x, y, x-1, y, generate_weight())
                if x < width - 1:
                    g.add_edge(x, y, x+1, y, generate_weight())
                if y > 0:
                    g.add_edge(x, y, x, y-1, generate_weight())
                if y < height -1:
                    g.add_edge(x, y, x, y+1, generate_weight())

        for x in range(width):
            for y in range(height):
                if random() < hard_obstacles_density:
                    g.remove_vertex(x, y)

        g.show_graph()

        dists, prevs = Dijkstra.solve(g)
        path = Dijkstra.build_path(g, prevs)

    g.show_graph(path=path)
    Graph.save_graph(g, "test")


if __name__ == "__main__":
    generate_graph(30, 30, hard_obstacles_density=0.2, soft_obstacles_density=0.5)
