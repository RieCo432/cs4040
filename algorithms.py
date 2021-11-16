import numpy as np


def Dijkstra(graph):
    dist = np.full(graph.vertices.flatten().shape, np.inf)
    Q = np.array([vertex for vertex in graph.vertices.flatten()])
    prev = np.full(graph.vertices.flatten().shape, None)
    dist[graph.vertices[graph.start].pos] = 0

    while any(Q):
        min_dist = np.inf
        min_index = None
        for i in [vertex.pos for vertex in Q if vertex]:
            if dist[i] < min_dist:
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