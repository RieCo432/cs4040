from graph_generator import generate_graph

graph_sizes = [20, 50, 100, 150, 200]
styles = [
    (0.1, 0), (0.2, 0), (0.3, 0), (0.4, 0),
    (0, 0.15), (0, 0.3), (0, 0.45), (0, 0.6),
    (0.1, 0.15), (0.2, 0.3), (0.3, 0.45), (0.4, 0.6)]

number_of_maps_per_config = 10


if __name__ == "__main__":
    for graph_size in graph_sizes:
        for style in styles:
            for i in range(number_of_maps_per_config):
                generate_graph(graph_size,
                               graph_size,
                               hard_obstacles_density=style[0],
                               soft_obstacles_density=style[1],
                               name=str(graph_size)+"x"+str(graph_size)+"hard"+str(style[0])+"soft"+str(style[1])+"count"+str(i))
