from Graph import Graph
from algorithms import Dijkstra

g = Graph.load_graph("test")

g.show_graph()

dists, prevs = Dijkstra.solve(g)
g.show_graph(path=Dijkstra.build_path(g, prevs))

