from Graph import Graph
from algorithms import Dijkstra

g = Graph(3, 3)

for i in range(3):
    for j in range(3):
        g.add_vertex(i, j)

# Node 0,0
g.add_edge(0, 0, 1, 0, 0)
g.add_edge(0, 0, 0, 1, 10)

# Node 1,0
g.add_edge(1, 0, 0, 0, 20)
g.add_edge(1, 0, 2, 0, 30)
g.add_edge(1, 0, 1, 1, 40)

# Node 2,0
g.add_edge(2, 0, 1, 0, 50)
g.add_edge(2, 0, 2, 1, 60)

# Node 0,1
g.add_edge(0, 1, 0, 0, 70)
g.add_edge(0, 1, 0, 2, 80)
g.add_edge(0, 1, 1, 1, 90)

# Node 1,1
g.add_edge(1, 1, 1, 0, 100)
g.add_edge(1, 1, 2, 1, 120)
g.add_edge(1, 1, 1, 2, 130)
g.add_edge(1, 1, 0, 1, 140)

# Node 2,1
g.add_edge(2, 1, 2, 0, 150)
g.add_edge(2, 1, 2, 2, 160)
g.add_edge(2, 1, 1, 1, 170)

# Node 0,2
g.add_edge(0, 2, 0, 1, 180)
g.add_edge(0, 2, 1, 2, 190)

# Node 1,2
g.add_edge(1, 2, 1, 1, 200)
g.add_edge(1, 2, 2, 2, 210)
g.add_edge(1, 2, 0, 2, 220)

# Node 2,2
g.add_edge(2, 2, 2, 1, 230)
g.add_edge(2, 2, 1, 2, 240)

g.remove_vertex(1, 0)
g.remove_vertex(1, 1)
g.remove_vertex(1, 2)

g.show_graph()

Graph.save_graph(g, "test")

dists, prevs = Dijkstra.solve(g)
path = Dijkstra.build_path(g, prevs)
if len(path) == 0:
    print("No path found")
else:
    g.show_graph(path=path)