from Graph import Graph
from algorithms import Dijkstra, AStar, HPAStar, FringeSearch
from random import random, randint
import numpy as np
from datetime import datetime


def generate_graph(width, height, hard_obstacles_density=0.0, soft_obstacles_density=0.0, name=None):  #, soft_obstacle_min=0, soft_obstacle_max=255, distribution="equal"):

    g = None
    path = []

    def generate_weight():
        if random() < soft_obstacles_density:
            return np.random.normal(loc=128, scale=16)
        else:
            return 10

    while len(path) == 0:

        print("Instantiating Graph")
        g = Graph(width, height)

        print("Adding vertices")
        for x in range(width):
            for y in range(height):
                g.add_vertex(x, y)

        print("Adding edges")
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

        print("Blocking vertices")
        for x in range(width):
            for y in range(height):
                if random() < hard_obstacles_density:
                    g.remove_vertex(x, y)

        print("Setting start and end")
        while not g.set_start(randint(0, width // 2), randint(0, height // 2)):
            pass
        while not g.set_end(randint(width // 2, width - 1), randint(height // 2, height - 1)):
            pass

        print("Checking path existence")
        #path, dist = Dijkstra.solve(g)
        path, dist = AStar.solve(g)

    g.show_graph()
    if name is None:
        Graph.save_graph(g, "test")
    else:
        Graph.save_graph(g, name)

    return g


if __name__ == "__main__":
    if True:
        g = generate_graph(100, 100, hard_obstacles_density=0.3, soft_obstacles_density=0.7)

        start = datetime.now()
        path, dist = Dijkstra.solve(g)
        end = datetime.now()
        elapsed = (end - start).total_seconds()
        print(elapsed)
        g.show_graph(path=path, title="{:10s}{:10.2f}".format("Dijkstra", dist))
        print("{:10s}{:10.2f}".format("Dijkstra", dist))

        path, dist = AStar.solve(g)
        g.show_graph(path=path, title="{:10s}{:10.2f}".format("A*", dist))
        print("{:10s}{:10.2f}".format("A*", dist))

        path, dist = HPAStar.solve(g)
        g.show_graph(path=path, title="{:10s}{:10.2f}".format("HPA*", dist))
        print("{:10s}{:10.2f}".format("HPA*", dist))

        path, dist = FringeSearch.solve(g)
        g.show_graph(path=path, title="{:10s}{:10.2f}".format("FringeSearch", dist))
        print("{:10s}{:10.2f}".format("FringeSearch", dist))
