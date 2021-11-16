import numpy as np


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

        return dist, prev

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
