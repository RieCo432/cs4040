from algorithms import Dijkstra, AStar, HPAStar, FringeSearch
from create_all_maps import graph_sizes, styles, number_of_maps_per_config
import json
from datetime import datetime
from Graph import Graph

algos = ["dijkstra", "astar", "hpastar", "fringe"]
runs_per_map = 25

if __name__ == "__main__":
    with open("results.json", "r") as infile:
        timings = json.load(infile)
    counter = 0
    for graph_size in graph_sizes:
        if "size"+str(graph_size) not in timings:
            timings["size"+str(graph_size)] = {}
        for style in styles:
            if "hard"+str(style[0]) not in timings["size"+str(graph_size)]:
                timings["size"+str(graph_size)]["hard"+str(style[0])] = {}
            if "soft"+str(style[1]) not in timings["size"+str(graph_size)]["hard"+str(style[0])]:
                timings["size" + str(graph_size)]["hard" + str(style[0])]["soft"+str(style[1])] = {}

            for i in range(number_of_maps_per_config):
                if str(i) not in timings["size" + str(graph_size)]["hard" + str(style[0])]["soft"+str(style[1])]:
                    timings["size" + str(graph_size)]["hard" + str(style[0])]["soft" + str(style[1])][str(i)] = {}

                graph = Graph.load_graph(str(graph_size)+"x"+str(graph_size)+"hard"+str(style[0])+"soft"+str(style[1])+"count"+str(i))

                for algo in algos:
                    if algo not in timings["size" + str(graph_size)]["hard" + str(style[0])]["soft"+str(style[1])][str(i)]:
                        timings["size" + str(graph_size)]["hard" + str(style[0])]["soft" + str(style[1])][str(i)][algo] = {}
                        timings["size" + str(graph_size)]["hard" + str(style[0])]["soft" + str(style[1])][str(i)][algo]["dists"] = []
                        timings["size" + str(graph_size)]["hard" + str(style[0])]["soft" + str(style[1])][str(i)][algo]["timings"] = []
                    for j in range(runs_per_map - len(timings["size" + str(graph_size)]["hard" + str(style[0])]["soft" + str(style[1])][str(i)][algo]["dists"])):
                        if algo == "dijkstra":
                            start = datetime.now()
                            path, dist = Dijkstra.solve(graph)
                            end = datetime.now()
                            timings["size" + str(graph_size)]["hard" + str(style[0])]["soft" + str(style[1])][str(i)][algo][
                                "dists"].append(dist)
                            timings["size" + str(graph_size)]["hard" + str(style[0])]["soft" + str(style[1])][str(i)][algo][
                                "timings"].append((end - start).total_seconds())
                        elif algo == "astar":
                            start = datetime.now()
                            path, dist = AStar.solve(graph)
                            end = datetime.now()
                            timings["size" + str(graph_size)]["hard" + str(style[0])]["soft" + str(style[1])][str(i)][algo][
                                "dists"].append(dist)
                            timings["size" + str(graph_size)]["hard" + str(style[0])]["soft" + str(style[1])][str(i)][algo][
                                "timings"].append((end - start).total_seconds())
                        elif algo == "hpastar":
                            start = datetime.now()
                            path, dist = HPAStar.solve(graph)
                            end = datetime.now()
                            timings["size" + str(graph_size)]["hard" + str(style[0])]["soft" + str(style[1])][str(i)][algo][
                                "dists"].append(dist)
                            timings["size" + str(graph_size)]["hard" + str(style[0])]["soft" + str(style[1])][str(i)][algo][
                                "timings"].append((end - start).total_seconds())

                        elif algo == "fringe":
                            start = datetime.now()
                            path, dist = FringeSearch.solve(graph)
                            end = datetime.now()
                            timings["size" + str(graph_size)]["hard" + str(style[0])]["soft" + str(style[1])][str(i)][algo][
                                "dists"].append(dist)
                            timings["size" + str(graph_size)]["hard" + str(style[0])]["soft" + str(style[1])][str(i)][algo][
                                "timings"].append((end - start).total_seconds())

                        counter += 1
                        if counter % 100 == 0:
                            print("Counter:", counter)

                        with open("results.json", "w") as outfile:
                            json.dump(timings, outfile)
