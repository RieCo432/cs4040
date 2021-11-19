from Graph import Graph
from algorithms import HPAStar, Dijkstra, AStar

g = Graph.load_graph("test")

g.show_graph()


path, dist = Dijkstra.solve(g)
g.show_graph(path=path, title="{:10s}{:10.2f}".format("Dijkstra", dist))

path, dist = AStar.solve(g)
g.show_graph(path=path, title="{:10s}{:10.2f}".format("A*", dist))

path, dist = HPAStar.solve(g)
g.show_graph(path=path, title="{:10s}{:10.2f}".format("HPA*", dist))

