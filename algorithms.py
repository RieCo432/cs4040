import numpy as np
from operator import attrgetter

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
                return AStar.build_path(cameFrom, current, graph), fScore[graph.end_index]
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
    def build_path(cameFrom, current, graph):
        path = [current]
        while cameFrom[current.pos] is not None:
            current = cameFrom[current.pos]
            path.insert(0, current)
        return path


