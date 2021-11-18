from Graph import Graph
from algorithms import HPAStar

g = Graph.load_graph("test")

g.show_graph()

HPAStar.breakupGraph(g)

