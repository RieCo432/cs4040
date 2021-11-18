import numpy as np
from operator import attrgetter
from math import floor
from Graph import Graph

class Dijkstra:

    @staticmethod
    def solve(graph):
        dist = np.full(graph.vertices.flatten().shape, np.inf)
        Q = np.array([vertex if not vertex.blocked else False for vertex in graph.vertices.flatten()])
        prev = np.full(graph.vertices.flatten().shape, None)
        dist[graph.vertices[graph.start].pos] = 0

        while any(Q):
            min_dist = np.inf
            min_index = None
            valid_indexes = [vertex.pos for vertex in Q if vertex]
            for i in valid_indexes:
                if dist[i] <= min_dist:
                    min_dist = dist[i]
                    min_index = i

            u = Q[min_index]
            Q[u.pos] = False

            for v in [edge.to_vertex for edge in u.edges if edge.to_vertex in Q]:
                alt = dist[u.pos] + u.get_weight_to(v)
                if alt < dist[v.pos]:
                    dist[v.pos] = alt
                    prev[v.pos] = u

        return Dijkstra.build_path(graph, prev), dist[graph.end_index]

    @staticmethod
    def build_path(graph, prevs):
        current_index = graph.end_index
        if prevs[current_index] is None:
            return []
        path = [graph.vertices[graph.end]]
        while current_index != graph.start_index:
            path.insert(0, prevs[current_index])
            current_index = prevs[current_index].pos
        return path


class AStar:

    @staticmethod
    def solve(graph):
        def h(from_coordinate):
            return ((
                    abs(from_coordinate[0] - graph.end[0])
                    + abs(from_coordinate[1] - graph.end[1])
            ) * 10)
        openSet = [graph.vertices[graph.start]]
        cameFrom = np.full(graph.vertices.flatten().shape, None)
        gScore = np.full(graph.vertices.flatten().shape, np.inf)
        gScore[graph.start_index] = 0
        fScore = np.full(graph.vertices.flatten().shape, np.inf)
        fScore[graph.start_index] = h(graph.start)

        while len(openSet) > 0:
            current = min(openSet, key=lambda v: fScore[v.pos])
            if current.pos == graph.end_index:
                return AStar.build_path(cameFrom, current), fScore[graph.end_index]
            openSet.remove(current)
            for edge in current.edges:
                tentative_gScore = gScore[current.pos] + edge.weight
                if tentative_gScore < gScore[edge.to_vertex.pos]:
                    cameFrom[edge.to_vertex.pos] = current
                    gScore[edge.to_vertex.pos] = tentative_gScore
                    fScore[edge.to_vertex.pos] = gScore[edge.to_vertex.pos] + h(graph.get_vertex_coordinates(edge.to_vertex))

                    if edge.to_vertex not in openSet:
                        openSet.append(edge.to_vertex)

        return [], None

    @staticmethod
    def build_path(cameFrom, current):
        path = [current]
        while cameFrom[current.pos] is not None:
            current = cameFrom[current.pos]
            path.insert(0, current)
        return path


class HPAStar:

    chunksize = 5

    @staticmethod
    def breakupGraph(graph):
        exchange_vertices = [graph.start, graph.end]
        chunk_outs = np.full((int(graph.vertices.shape[0] / HPAStar.chunksize), int(graph.vertices.shape[1] / HPAStar.chunksize)), None)
        for x in range(0, graph.vertices.shape[0], HPAStar.chunksize):
            for y in range(0, graph.vertices.shape[1], HPAStar.chunksize):
                chunk_outs[x // HPAStar.chunksize, y // HPAStar.chunksize] = {}
                mini_graph = Graph(5, 5)
                mini_graph.vertices = graph.vertices[x:x+5, y:y+5]
                mini_graph.show_graph()

                chunknorthouts_all = [(x + i,y) if graph.vertices[x + i, y].north is not None else None for i in range(HPAStar.chunksize) ]
                chunknorthouts = []
                if any(chunknorthouts_all):
                    start = None
                    for i in range(HPAStar.chunksize):
                        if chunknorthouts_all[i] is not None and start is None:
                            start = i
                        if (i == HPAStar.chunksize - 1 or chunknorthouts_all[i+1] is None) and start is not None:
                            chunknorthouts.append(graph.get_vertex_coordinates(min(
                                [graph.vertices[chunknorthouts_all[c]] for c in range(start, i+1)],
                                key=lambda v: v.north.weight)))
                            start = None

                    #for p in chunknorthouts:
                    #    if p is not None:
                    #        graph.vertices[p].north.weight = 255
                chunk_outs[x//HPAStar.chunksize, y//HPAStar.chunksize]["north"] = chunknorthouts

                chunksouthouts_all = [(x + i, y+4) if graph.vertices[x + i, y+4].south is not None else None for i in range(HPAStar.chunksize)]
                chunksouthouts = []
                if any(chunksouthouts_all):
                    start = None
                    for i in range(HPAStar.chunksize):
                        if chunksouthouts_all[i] is not None and start is None:
                            start = i
                        if (i == HPAStar.chunksize - 1 or chunksouthouts_all[i + 1] is None) and start is not None:
                            chunksouthouts.append(graph.get_vertex_coordinates(min(
                                [graph.vertices[chunksouthouts_all[c]] for c in range(start, i + 1)],
                                key=lambda v: v.south.weight)))
                            start = None

                    # for p in chunksouthouts:
                    #     if p is not None:
                    #         graph.vertices[p].south.weight = 255

                chunk_outs[x // HPAStar.chunksize, y // HPAStar.chunksize]["south"] = chunksouthouts


                chunkwestouts_all = [(x, y + i) if graph.vertices[x, y + i].west is not None else None for i in range(HPAStar.chunksize)]
                chunkwestouts = []
                if any(chunkwestouts_all):
                    start = None
                    for i in range(HPAStar.chunksize):
                        if chunkwestouts_all[i] is not None and start is None:
                            start = i
                        if (i == HPAStar.chunksize - 1 or chunkwestouts_all[i + 1] is None) and start is not None:
                            chunkwestouts.append(graph.get_vertex_coordinates(min(
                                [graph.vertices[chunkwestouts_all[c]] for c in range(start, i + 1)],
                                key=lambda v: v.west.weight)))
                            start = None

                    # for p in chunkwestouts:
                    #     if p is not None:
                    #         graph.vertices[p].west.weight = 255

                chunk_outs[x // HPAStar.chunksize, y // HPAStar.chunksize]["west"] = chunkwestouts

                chunkeastouts_all = [(x+4, y + i) if graph.vertices[x+4, y + i].east is not None else None for i in range(HPAStar.chunksize)]
                chunkeastouts = []
                if any(chunkeastouts_all):
                    start = None
                    for i in range(HPAStar.chunksize):
                        if chunkeastouts_all[i] is not None and start is None:
                            start = i
                        if (i == HPAStar.chunksize - 1 or chunkeastouts_all[i + 1] is None) and start is not None:
                            chunkeastouts.append(graph.get_vertex_coordinates(min(
                                [graph.vertices[chunkeastouts_all[c]] for c in range(start, i + 1)],
                                key=lambda v: v.east.weight)))
                            start = None

                    # for p in chunkeastouts:
                    #     if p is not None:
                    #         graph.vertices[p].east.weight = 255

                chunk_outs[x // HPAStar.chunksize, y // HPAStar.chunksize]["east"] = chunkeastouts

        graph.show_graph()