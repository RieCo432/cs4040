from Graph import Graph
from evaluate_all_algos import styles, number_of_maps_per_config
from algorithms import AStar, HPAStar, FringeSearch, Dijkstra

# candidates = []
#
# graph_sizes = [20, 50]
# for graph_size in graph_sizes:
#     for style in styles:
#         for num in range(number_of_maps_per_config):
#             graph = Graph.load_graph(str(graph_size)+"x"+str(graph_size)+"hard"+str(style[0])+"soft"+str(style[1])+"count"+str(num))
#             #graph.show_graph("Example Graph, Size: {}x{}, Hard Obstacles: {}%, Soft Obstacles: {}%".format(graph_size, graph_size, int(100*style[0]), int(100*style[1])))
#
#             dijkstra_path, dijkstra_dist = Dijkstra.solve(graph)
#             astar_path, astar_dist = AStar.solve(graph)
#             hpastar_path, hpastar_dist = HPAStar.solve(graph)
#             fringe_path, fringe_dist = FringeSearch.solve(graph)
#
#             path1 = dijkstra_path
#             algos1 = ["dijkstra"]
#             path2 = []
#             algos2 = []
#             path3 = []
#             algos3 = []
#             path4 = []
#             algos4 = []
#             if astar_path == path1:
#                 algos1.append("astar")
#             else:
#                 path2 = astar_path
#                 algos2.append("astar")
#
#             if hpastar_path == path1:
#                 algos1.append("hpastar")
#             elif hpastar_path == path2:
#                 algos2.append("hpastar")
#             else:
#                 path3 = hpastar_path
#                 algos3.append("hpastar")
#
#             if fringe_path == path1:
#                 algos1.append("fringe")
#             elif fringe_path == path2:
#                 algos2.append("fringe")
#             elif fringe_path == path3:
#                 algos3.append("fringe")
#             else:
#                 path4 = fringe_path
#                 algos4.append("fringe")
#
#             print(algos1, algos2, algos3, algos4)
#             if len(algos1) == 3:
#                 candidates.append(str(graph_size)+"x"+str(graph_size)+"hard"+str(style[0])+"soft"+str(style[1])+"count"+str(num))
#
# print(candidates)
#

# candidates = ['20x20hard0.2soft0count1', '20x20hard0.2soft0count7', '20x20hard0.3soft0count1', '20x20hard0.4soft0count0', '20x20hard0.4soft0count3', '20x20hard0soft0.45count1', '20x20hard0soft0.45count4', '20x20hard0soft0.45count7', '20x20hard0soft0.6count2', '20x20hard0soft0.6count6', '20x20hard0soft0.6count7', '20x20hard0soft0.6count8', '20x20hard0.2soft0.3count9', '20x20hard0.3soft0.45count0', '20x20hard0.3soft0.45count1', '20x20hard0.3soft0.45count2', '20x20hard0.3soft0.45count3', '20x20hard0.3soft0.45count4', '20x20hard0.3soft0.45count8', '20x20hard0.3soft0.45count9', '20x20hard0.4soft0.6count0', '20x20hard0.4soft0.6count6', '20x20hard0.4soft0.6count7', '20x20hard0.4soft0.6count8', '20x20hard0.4soft0.6count9', '50x50hard0soft0.6count0', '50x50hard0soft0.6count6', '50x50hard0.3soft0.45count6', '50x50hard0.3soft0.45count7', '50x50hard0.4soft0.6count0', '50x50hard0.4soft0.6count1', '50x50hard0.4soft0.6count2', '50x50hard0.4soft0.6count3', '50x50hard0.4soft0.6count6', '50x50hard0.4soft0.6count7', '50x50hard0.4soft0.6count8', '50x50hard0.4soft0.6count9']
#
# final_candiates = []
#
# for candidate in candidates:
#     graph = Graph.load_graph(candidate)
#     graph.show_graph()
#     keep = input("Keep? y/n") == "y"
#     if keep:
#         final_candiates.append(candidate)
#
# print(final_candiates)

final_candidates = ['20x20hard0.2soft0count1', '20x20hard0.3soft0count1', '20x20hard0.4soft0count3', '20x20hard0soft0.45count1', '20x20hard0soft0.45count4', '20x20hard0soft0.6count2', '20x20hard0soft0.6count8', '20x20hard0.3soft0.45count0', '20x20hard0.3soft0.45count1', '20x20hard0.3soft0.45count2', '20x20hard0.3soft0.45count3', '20x20hard0.3soft0.45count9', '20x20hard0.4soft0.6count7', '20x20hard0.4soft0.6count8']
MAYBE = ['50x50hard0soft0.6count6', '50x50hard0.3soft0.45count6', '50x50hard0.3soft0.45count7', '50x50hard0.4soft0.6count0', '50x50hard0.4soft0.6count1', '50x50hard0.4soft0.6count3', '50x50hard0.4soft0.6count6', '50x50hard0.4soft0.6count7', '50x50hard0.4soft0.6count8', '50x50hard0.4soft0.6count9']
chosen = ['20x20hard0.4soft0count3', '20x20hard0soft0.6count2', '20x20hard0.3soft0.45count1']


for candidate in chosen:
    graph = Graph.load_graph(candidate)
    path1, dist1 = AStar.solve(graph)
    path2, dist2 = HPAStar.solve(graph)

    title = "Example; "
    if "20x20" in candidate:
        title += "Size:20x20,"
    elif "50x50" in candidate:
        title += "Size:50x50,"

    if "hard0.4" in candidate:
        title += "Hard obstacles: 40%,"
    elif "hard0.3" in candidate:
        title += "Hard obstacles: 30%,"
    elif "hard0.2" in candidate:
        title += "Hard obstacles: 20%,"
    elif "hard0.1" in candidate:
        title += "Hard obstacles: 10%,"
    elif "hard0" in candidate:
        title += "Hard obstacles: 0%,"

    if "soft0.6" in candidate:
        title += "Soft obstacles: 60%"
    elif "soft0.45" in candidate:
        title += "Soft obstacles: 45%"
    elif "soft0.3" in candidate:
        title += "Soft obstacles: 30%"
    elif "soft0.15" in candidate:
        title += "Soft obstacles: 15%"
    elif "soft0" in candidate:
        title += "Soft obstacles: 0%"

    graph.show_graph(title=title)
    graph.show_graph(path=path1, title="Solution by Dijkstra, A* and Fringe Search: {}".format(dist1))
    graph.show_graph(path=path2, title="Solution by HPA*: {}".format(dist2))

    input("Next")

