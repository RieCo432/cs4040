from datetime import datetime

import numpy as np
from Graph import Graph
from DoubleLinkedList import DoubleLinkedList


class Dijkstra:

    @staticmethod
    def solve(graph):
        dist = np.full(graph.vertices.flatten().shape, np.inf)
        Q = np.array([vertex if not vertex.blocked else False for vertex in graph.vertices.flatten()])
        prev = np.full(graph.vertices.flatten().shape, None)
        dist[graph.vertices[graph.start].pos] = 0

        while any(Q):
            # left = len([1 for v in Q if v])
            # if left % 1000 == 0:
            #     print(left, "vertices to go")
            min_dist = np.inf
            min_index = None
            for v in Q[np.where(Q)]:
                if dist[v.pos] <= min_dist:
                    min_dist = dist[v.pos]
                    min_index = v.pos

            u = Q[min_index]
            Q[u.pos] = False

            for v in [edge.to_vertex for edge in u.edges if Q[edge.to_vertex.pos]]:
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
    def solve(graph):
        chunks = np.full((int(graph.vertices.shape[0] / HPAStar.chunksize), int(graph.vertices.shape[1] / HPAStar.chunksize)), None)
        chunk_outs = np.empty((int(graph.vertices.shape[0] / HPAStar.chunksize), int(graph.vertices.shape[1] / HPAStar.chunksize)), dtype=object)
        chunk_ins = np.empty((int(graph.vertices.shape[0] / HPAStar.chunksize), int(graph.vertices.shape[1] / HPAStar.chunksize)), dtype=object)

        for x in range(chunk_outs.shape[0]):
            for y in range(chunk_outs.shape[1]):
                chunk_outs[x, y] = []
                chunk_ins[x, y] = []

        for x in range(0, graph.vertices.shape[0], HPAStar.chunksize):
            for y in range(0, graph.vertices.shape[1], HPAStar.chunksize):

                mini_graph = Graph(HPAStar.chunksize, HPAStar.chunksize)
                for i in range(mini_graph.vertices.shape[0]):
                    for j in range(mini_graph.vertices.shape[1]):
                        mini_graph.add_vertex(i, j)

                for i in range(mini_graph.vertices.shape[0]):
                    for j in range(mini_graph.vertices.shape[1]):
                        if graph.vertices[x+i, y+j].north is not None and j != 0:
                            mini_graph.add_edge(i, j, i, j - 1, graph.vertices[x+i, y+j].north.weight)
                        if graph.vertices[x+i, y+j].south is not None and j != HPAStar.chunksize-1:
                            mini_graph.add_edge(i, j, i, j + 1, graph.vertices[x+i, y+j].south.weight)
                        if graph.vertices[x+i, y+j].west is not None and i != 0:
                            mini_graph.add_edge(i, j, i - 1, j, graph.vertices[x+i, y+j].west.weight)
                        if graph.vertices[x+i, y+j].east is not None and i != HPAStar.chunksize-1:
                            mini_graph.add_edge(i, j, i + 1, j, graph.vertices[x+i, y+j].east.weight)

                        mini_graph.vertices[i, j].update_edges()

                for i in range(mini_graph.vertices.shape[0]):
                    for j in range(mini_graph.vertices.shape[1]):
                        if graph.vertices[x+i, y+j].blocked:
                            mini_graph.remove_vertex(i, j)

                chunks[x // HPAStar.chunksize, y // HPAStar.chunksize] = mini_graph

                chunknorthouts_all = [(x + i,y) if graph.vertices[x + i, y].north is not None else None for i in range(HPAStar.chunksize) ]
                if any(chunknorthouts_all):
                    start = None
                    for i in range(HPAStar.chunksize):
                        if chunknorthouts_all[i] is not None and start is None:
                            start = i
                        if (i == HPAStar.chunksize - 1 or chunknorthouts_all[i+1] is None) and start is not None:
                            vertex = graph.get_vertex_coordinates(min(
                                [graph.vertices[chunknorthouts_all[c]] for c in range(start, i+1)],
                                key=lambda v: v.north.weight))
                            chunk_outs[x // HPAStar.chunksize, y // HPAStar.chunksize].append(vertex)
                            chunk_ins[x // HPAStar.chunksize, y // HPAStar.chunksize - 1].append(vertex)
                            start = None

                chunksouthouts_all = [(x + i, y+HPAStar.chunksize-1) if graph.vertices[x + i, y+HPAStar.chunksize-1].south is not None else None for i in range(HPAStar.chunksize)]
                if any(chunksouthouts_all):
                    start = None
                    for i in range(HPAStar.chunksize):
                        if chunksouthouts_all[i] is not None and start is None:
                            start = i
                        if (i == HPAStar.chunksize - 1 or chunksouthouts_all[i + 1] is None) and start is not None:
                            vertex = graph.get_vertex_coordinates(min(
                                [graph.vertices[chunksouthouts_all[c]] for c in range(start, i + 1)],
                                key=lambda v: v.south.weight))
                            chunk_outs[x // HPAStar.chunksize, y // HPAStar.chunksize].append(vertex)
                            chunk_ins[x // HPAStar.chunksize, y // HPAStar.chunksize + 1].append(vertex)
                            start = None

                chunkwestouts_all = [(x, y + i) if graph.vertices[x, y + i].west is not None else None for i in range(HPAStar.chunksize)]
                if any(chunkwestouts_all):
                    start = None
                    for i in range(HPAStar.chunksize):
                        if chunkwestouts_all[i] is not None and start is None:
                            start = i
                        if (i == HPAStar.chunksize - 1 or chunkwestouts_all[i + 1] is None) and start is not None:
                            vertex = graph.get_vertex_coordinates(min(
                                [graph.vertices[chunkwestouts_all[c]] for c in range(start, i + 1)],
                                key=lambda v: v.west.weight))
                            chunk_outs[x // HPAStar.chunksize, y // HPAStar.chunksize].append(vertex)
                            chunk_ins[x // HPAStar.chunksize - 1, y // HPAStar.chunksize].append(vertex)
                            start = None

                chunkeastouts_all = [(x+HPAStar.chunksize-1, y + i) if graph.vertices[x+HPAStar.chunksize-1, y + i].east is not None else None for i in range(HPAStar.chunksize)]
                if any(chunkeastouts_all):
                    start = None
                    for i in range(HPAStar.chunksize):
                        if chunkeastouts_all[i] is not None and start is None:
                            start = i
                        if (i == HPAStar.chunksize - 1 or chunkeastouts_all[i + 1] is None) and start is not None:
                            vertex = graph.get_vertex_coordinates(min(
                                [graph.vertices[chunkeastouts_all[c]] for c in range(start, i + 1)],
                                key=lambda v: v.east.weight))
                            chunk_outs[x // HPAStar.chunksize, y // HPAStar.chunksize].append(vertex)
                            chunk_ins[x // HPAStar.chunksize + 1, y // HPAStar.chunksize].append(vertex)
                            start = None

        chunk_ins[graph.start[0] // HPAStar.chunksize, graph.start[1] // HPAStar.chunksize].append(graph.start)
        chunk_outs[graph.end[0] // HPAStar.chunksize, graph.end[1] // HPAStar.chunksize].append(graph.end)

        abstract_graph = Graph(graph.vertices.shape[0], graph.vertices.shape[1])
        for outs in chunk_outs.flatten():
            for out in outs:
                abstract_graph.add_vertex(out[0], out[1])
        abstract_graph.add_vertex(graph.start[0], graph.start[1])
        abstract_graph.set_start(graph.start[0], graph.start[1])
        abstract_graph.set_end(graph.end[0], graph.end[1])

        path_segments = {}

        for x_chunk in range(graph.vertices.shape[0] // HPAStar.chunksize):
            for y_chunk in range(graph.vertices.shape[1] // HPAStar.chunksize):
                chunk = chunks[x_chunk, y_chunk]
                for chunk_in in chunk_ins[x_chunk, y_chunk]:
                    if str(chunk_in) not in path_segments:
                        path_segments[str(chunk_in)] = {}
                    start = chunk_in
                    inter_dist = 0
                    if chunk_in[0] == x_chunk * HPAStar.chunksize - 1:
                        inter_dist = graph.vertices[chunk_in].east.weight
                        start = (chunk_in[0]+1, chunk_in[1])
                    elif chunk_in[0] == (x_chunk + 1) * HPAStar.chunksize:
                        inter_dist = graph.vertices[chunk_in].west.weight
                        start = (chunk_in[0]-1, chunk_in[1])
                    elif chunk_in[1] == y_chunk * HPAStar.chunksize - 1:
                        inter_dist = graph.vertices[chunk_in].south.weight
                        start = (chunk_in[0], chunk_in[1]+1)
                    elif chunk_in[1] == (y_chunk + 1) * HPAStar.chunksize:
                        inter_dist = graph.vertices[chunk_in].north.weight
                        start = (chunk_in[0], chunk_in[1]-1)
                    chunk.set_start(start[0] % HPAStar.chunksize, start[1] % HPAStar.chunksize)
                    for end in chunk_outs[x_chunk, y_chunk]:
                        chunk.set_end(end[0] % HPAStar.chunksize, end[1] % HPAStar.chunksize)

                        path, dist = AStar.solve(chunk)
                        if dist is not np.inf and dist is not None:
                            abstract_graph.add_edge(chunk_in[0], chunk_in[1], end[0], end[1], inter_dist+dist,
                                                    allow_all=True)
                            path_segments[str(chunk_in)][str(end)] = []
                            for v in path:
                                x_mini, y_mini = chunk.get_vertex_coordinates(v)
                                x = x_mini + x_chunk * HPAStar.chunksize
                                y = y_mini + y_chunk * HPAStar.chunksize
                                path_segments[str(chunk_in)][str(end)].append(graph.vertices[x, y])

        path_abstract, dist = AStar.solve(abstract_graph)

        path = []
        for i in range(len(path_abstract) - 1):
            f = str(graph.get_vertex_coordinates(path_abstract[i]))
            t = str(graph.get_vertex_coordinates(path_abstract[i+1]))
            segment = path_segments[f][t]
            for vertex in segment:
                path.append(vertex)

        return path, dist


class FringeSearch:

    @staticmethod
    def solve(graph):
        # total_list_time = 0
        def h(from_coordinate):
            return ((
                            abs(from_coordinate[0] - graph.end[0])
                            + abs(from_coordinate[1] - graph.end[1])
                    ) * 10)

        F = [graph.start_index]
        #now = [graph.start_index]
        #later = []
        C = np.full(graph.vertices.flatten().shape, None)
        index_in_list = np.full(graph.vertices.flatten().shape, False)
        index_in_list[graph.start_index] = True
        C[graph.start_index] = (0, None)
        flimit = h(graph.start)

        while len(F) > 0:
            fmin = np.inf
            i = 0
            while i < len(F):
                index = F[i]
                (g, parent) = C[index]
                f = g + h(graph.get_vertex_coordinates_from_pos(index))
                if f > flimit:
                    fmin = min(f, fmin)
                    index_in_list[index] = False
                    i += 1
                    continue

                if index == graph.end_index:
                    #print("list time:", total_list_time)
                    return FringeSearch.build_path(graph, C)

                for edge in sorted(graph.vertices[graph.get_vertex_coordinates_from_pos(index)].edges,
                                   key=lambda e: e.weight, reverse=True):
                    g_child = g + edge.weight
                    if C[edge.to_vertex.pos] is not None:
                        (g_cached, parent) = C[edge.to_vertex.pos]
                        if g_child >= g_cached:
                            continue
                    #s = datetime.now()
                    if index_in_list[edge.to_vertex.pos]:
                        F.remove(edge.to_vertex.pos)
                        index_in_list[edge.to_vertex.pos] = False

                    #total_list_time += (datetime.now() - s).total_seconds()
                    F.insert(i+1, edge.to_vertex.pos)
                    index_in_list[edge.to_vertex.pos] = True
                    C[edge.to_vertex.pos] = (g_child, index)
                F.__delitem__(i)
                index_in_list[index] = False

            flimit = fmin
            #now = later
            #later = []

        return [], None

    @staticmethod
    def build_path(graph, C):
        path = [graph.vertices[graph.end]]
        (g, parent) = C[graph.end_index]
        while parent is not None:
            path.insert(0, graph.vertices[graph.get_vertex_coordinates_from_pos(parent)])
            (_, parent) = C[parent]

        return path, g



