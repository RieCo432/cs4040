import json
from matplotlib import pyplot as plt
from evaluate_all_algos import runs_per_map, algos
from create_all_maps import graph_sizes, styles, number_of_maps_per_config
import numpy as np
from scipy import stats

with open("results - Copy.json", "r") as f:
    results = json.load(f)

colors = {"dijkstra": "red", "astar": "green", "hpastar": "blue", "fringe":"orange"}
display_names = {"dijkstra": "Dijkstra", "astar": "A*", "hpastar":"HPA*", "fringe": "FringeSearch"}
size_labels = [str(s)+"x"+str(s) for s in graph_sizes]

timings = {}
dists = {}

for algo in algos:
    timings[algo] = {}
    dists[algo] = {}
    for size in graph_sizes:
        timings[algo][size] = {}
        dists[algo][size] = {}
        for style in styles:
            timings[algo][size][str(style[0]) + ":" + str(style[1])] = []
            dists[algo][size][str(style[0]) + ":" + str(style[1])] = []
            for num in range(number_of_maps_per_config):
                try:
                    timings[algo][size][str(style[0]) + ":" + str(style[1])].append(np.mean(
                        results["size" + str(size)]["hard" + str(style[0])]["soft" + str(style[1])][str(num)][algo]["timings"]))
                    dists[algo][size][str(style[0]) + ":" + str(style[1])].append(np.mean(
                        results["size" + str(size)]["hard" + str(style[0])]["soft" + str(style[1])][str(num)][algo]["dists"]))
                except KeyError:
                    pass
                except TypeError:
                    dists[algo][size][str(style[0]) + ":" + str(style[1])].append(
                        results["size" + str(size)]["hard" + str(style[0])]["soft" + str(style[1])][str(num)][algo][
                            "dists"][0])
                    print(algo, size, style, num)

#print(timings)
#print(dists)

all_times_per_algo_and_size = {}
mean_times_per_algo_and_size = {}
total_time = 0
total_runs = 0

for algo in algos:
    all_times_per_algo_and_size[algo] = {}
    mean_times_per_algo_and_size[algo] = []
    for size, size_string in zip(graph_sizes, results):
        all_times_per_algo_and_size[algo][size] = []
        for hard in results[size_string]:
            for soft in results[size_string][hard]:
                for num in results[size_string][hard][soft]:
                    try:
                        all_times_per_algo_and_size[algo][size].append(np.mean(results[size_string][hard][soft][num][algo]["timings"]))
                        total_time += sum(results[size_string][hard][soft][num][algo]["timings"])
                        total_runs += len(results[size_string][hard][soft][num][algo]["timings"])
                    except KeyError:
                        pass
        mean_times_per_algo_and_size[algo].append(np.mean(all_times_per_algo_and_size[algo][size]))

print(total_time)
print(total_runs)

def plot_mean_runtimes_by_size(algos_to_show):
    for algo in algos_to_show:
        plt.plot(size_labels, mean_times_per_algo_and_size[algo], color=colors[algo], label=display_names[algo])
    plt.xlabel("Graph Size (vertices x vertices)")
    plt.ylabel("Runtime (s)")
    plt.xticks(size_labels)
    plt.legend(loc="upper left")
    #plt.title("Mean runtime by size")
    plt.show()


def show_runtime_distribution_by_size(algos_to_show, bins=None):
    for size, size_label in zip(graph_sizes, size_labels):
        if bins is None:
            plt.hist([all_times_per_algo_and_size[algo][size] for algo in algos_to_show],
                     color=[colors[algo] for algo in algos_to_show],
                     label=[display_names[algo] for algo in algos_to_show])
        else:
            plt.hist([all_times_per_algo_and_size[algo][size] for algo in algos_to_show],
                     color=[colors[algo] for algo in algos_to_show],
                     label=[display_names[algo] for algo in algos_to_show],
                     bins=bins)
        plt.xlabel("Runtime (s)")
        plt.ylabel("Frequency")
        plt.title("Graph size: {}x{}".format(size, size))
        plt.legend(loc="upper center")
        #plt.title("Runtime distribution for size" + size_label)
        plt.show()


reldistdiffs = {}

for algo in [algo for algo in algos if algo != "dijkstra"]:
    reldistdiffs[algo] = {}
    for size in graph_sizes:
        reldistdiff_for_size = []
        for style in styles:
            for num in range(number_of_maps_per_config):
                try:
                    dijkstra_dist = dists["dijkstra"][size][str(style[0])+":"+str(style[1])][num]
                    algo_dist = dists[algo][size][str(style[0])+":"+str(style[1])][num]
                    reldiff = (algo_dist - dijkstra_dist) / dijkstra_dist
                    #if dijkstra_dist != algo_dist:
                    #    print("dijkstra", dijkstra_dist, algo, algo_dist, "appending", reldiff)
                    reldistdiff_for_size.append(reldiff)
                except TypeError:
                    pass
                except IndexError:
                    pass
        reldistdiffs[algo][size] = np.mean(reldistdiff_for_size)

relativeruntimes = {}


for algo in algos:
    relativeruntimes[algo] = []
    for i, size in enumerate(graph_sizes):
        for_size = np.divide(all_times_per_algo_and_size[algo][size], mean_times_per_algo_and_size[algo][i])
        for t in for_size:
            relativeruntimes[algo].append(t)

# print(relativeruntimes)


def show_relative_runtime_distributions(algos_to_show, bins=None):
    if bins is None:
        plt.hist([relativeruntimes[algo] for algo in algos_to_show],
                     color=[colors[algo] for algo in algos_to_show],
                     label=[display_names[algo] for algo in algos_to_show])
    else:
        plt.hist([relativeruntimes[algo] for algo in algos_to_show],
                     color=[colors[algo] for algo in algos_to_show],
                     label=[display_names[algo] for algo in algos_to_show],
                     bins=bins)
    plt.xlabel("Relative runtime compared to mean")
    plt.ylabel("Frequency")
    plt.title("Relative runtime compared to mean")
    plt.legend(loc="upper right")
    plt.show()


def plot_relative_runtime_percentiles(algos_to_show, max_score=5.1, step=0.1):
    for algo in algos_to_show:
        percentiles = []
        for score in np.arange(0, max_score, step):
            percentiles.append(stats.percentileofscore(relativeruntimes[algo], score))
        plt.plot(np.arange(0, max_score, step), percentiles, color=colors[algo], label=display_names[algo])
    plt.xlabel("Relative runtime compared to mean")
    plt.ylabel("Percentile")
    #plt.xticks(np.arange())
    plt.legend(loc="lower right")
    # plt.title("Mean runtime by size")
    plt.show()

percentiles = [50, 75, 90, 99]
percentiles_of_relative_runtime = {}
for algo in algos:
    percentiles_of_relative_runtime[algo] = stats.scoreatpercentile(relativeruntimes[algo], percentiles)

##############################################
#        Actually included in report         #
##############################################
if True:
    print(stats.kruskal(all_times_per_algo_and_size["dijkstra"][20], all_times_per_algo_and_size["astar"][20],
                        all_times_per_algo_and_size["hpastar"][20], all_times_per_algo_and_size["fringe"][20]))
    print(stats.kruskal(all_times_per_algo_and_size["dijkstra"][50], all_times_per_algo_and_size["astar"][50],
                        all_times_per_algo_and_size["hpastar"][50], all_times_per_algo_and_size["fringe"][50]))
    print(stats.kruskal(all_times_per_algo_and_size["dijkstra"][100], all_times_per_algo_and_size["astar"][100],
                        all_times_per_algo_and_size["hpastar"][100], all_times_per_algo_and_size["fringe"][100]))
    print(stats.kruskal(all_times_per_algo_and_size["dijkstra"][150], all_times_per_algo_and_size["astar"][150],
                        all_times_per_algo_and_size["hpastar"][150], all_times_per_algo_and_size["fringe"][150]))
    print(stats.kruskal(all_times_per_algo_and_size["dijkstra"][200], all_times_per_algo_and_size["astar"][200],
                        all_times_per_algo_and_size["hpastar"][200], all_times_per_algo_and_size["fringe"][200]))

    print(stats.kruskal(all_times_per_algo_and_size["dijkstra"][20], all_times_per_algo_and_size["dijkstra"][50], all_times_per_algo_and_size["dijkstra"][100], all_times_per_algo_and_size["dijkstra"][150], all_times_per_algo_and_size["dijkstra"][200]))
    print(stats.kruskal(all_times_per_algo_and_size["astar"][20], all_times_per_algo_and_size["astar"][50], all_times_per_algo_and_size["astar"][100], all_times_per_algo_and_size["astar"][150], all_times_per_algo_and_size["astar"][200]))
    print(stats.kruskal( all_times_per_algo_and_size["hpastar"][20], all_times_per_algo_and_size["hpastar"][50], all_times_per_algo_and_size["hpastar"][100], all_times_per_algo_and_size["hpastar"][150], all_times_per_algo_and_size["hpastar"][200]))
    print(stats.kruskal(all_times_per_algo_and_size["fringe"][20], all_times_per_algo_and_size["fringe"][50], all_times_per_algo_and_size["fringe"][100], all_times_per_algo_and_size["fringe"][150], all_times_per_algo_and_size["fringe"][200]))

    print(reldistdiffs)
    print(mean_times_per_algo_and_size)

    plot_mean_runtimes_by_size(algos)
    plot_mean_runtimes_by_size([algo for algo in algos if algo != "dijkstra"])

    show_runtime_distribution_by_size(["hpastar"])
    show_runtime_distribution_by_size(["astar", "fringe"], bins=20)

    show_relative_runtime_distributions(["astar", "hpastar", "fringe", "dijkstra"], bins=12)
    plot_relative_runtime_percentiles(["astar", "dijkstra", "hpastar", "fringe"])

    print(percentiles_of_relative_runtime)

    pass

