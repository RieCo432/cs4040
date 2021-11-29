from Graph import Graph
from algorithms import HPAStar, Dijkstra, AStar, FringeSearch
from datetime import datetime

g = Graph.load_graph("test")

g.show_graph()


start = datetime.now()
path, dist = FringeSearch.solve(g)
end = datetime.now()
elapsed = (end - start).total_seconds()
print("Fringe", elapsed)
g.show_graph(path=path, title="{:10s}{:10.2f}".format("FringeSearch", dist))

start = datetime.now()
path, dist = AStar.solve(g)
end = datetime.now()
elapsed = (end - start).total_seconds()
print("A*", elapsed)

g.show_graph(path=path, title="{:10s}{:10.2f}".format("A*", dist))

# start = datetime.now()
# path, dist = HPAStar.solve(g)
# end = datetime.now()
# elapsed = (end - start).total_seconds()
# print("HPA*", elapsed)
#
# g.show_graph(path=path, title="{:10s}{:10.2f}".format("HPA*", dist))

# path, dist = HPAStar.solve(g)
# g.show_graph(path=path, title="{:10s}{:10.2f}".format("HPA*", dist))

