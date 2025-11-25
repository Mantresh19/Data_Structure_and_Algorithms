import os, sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
libraries_path = os.path.join(base_dir, "Libraries", "clrsPython")
sys.path.insert(0, libraries_path)
# Import Algorithm (CLRS)
from adjacency_list_graph import AdjacencyListGraph
from bfs import bfs

# Simple Dataset (5 Stations)
graph_dict = {
    'A': ['B'],           # A connects to B
    'B': ['A', 'C'],      # B connects to A and C
    'C': ['B', 'D'],      # C connects to B and D
    'D': ['C', 'E'],      # D connects to C and E
    'E': ['D']            # E connects to D
}

# List of station names
stations = list(graph_dict.keys())

# Map station names → numeric node IDs for the CLRS library
name_to_id = {name: idx for idx, name in enumerate(stations)}

# Reverse map: node IDs → station names
id_to_name = {idx: name for name, idx in name_to_id.items()}

# Build CLRS Graph (undirected)
def build_clrs_graph(graph_dict):
    card_V = len(graph_dict)  # number of vertices
    G = AdjacencyListGraph(card_V, directed=False, weighted=False)

    # Add edges to the CLRS graph
    for u in graph_dict:
        u_id = name_to_id[u]
        for v in graph_dict[u]:
            v_id = name_to_id[v]

            # Insert the edge if it is not already present
            if not G.has_edge(u_id, v_id):
                G.insert_edge(u_id, v_id)

    return G

# BFS Fewest Stops using CLRS BFS
def fewest_stops_path_clrs(graph_dict, start, goal):

    # Build the CLRS-style graph
    G = build_clrs_graph(graph_dict)

    # Convert names → integer IDs
    start_id = name_to_id[start]
    goal_id = name_to_id[goal]

    # Run CLRS BFS (returns: dist[], pi[])
    # dist[i] = shortest distance (#edges) from start
    # pi[i]   = parent of node i in shortest-path tree
    dist, pi = bfs(G, start_id)

    # Reconstruct path by walking backwards from the goal using parents
    path_ids = []
    current = goal_id
    while current is not None:   # None = no parent (root or unreachable)
        path_ids.insert(0, current)
        current = pi[current]

    # If path does NOT start at the start node, goal was unreachable
    if path_ids[0] != start_id:
        return None, None

    # Convert numeric node IDs → station names
    path_names = [id_to_name[i] for i in path_ids]

    # Number of stops = number of edges = path length - 1
    return path_names, len(path_ids) - 1

# Test Example
start_station = 'A'
goal_station = 'E'

# Compute BFS shortest path
path, stops = fewest_stops_path_clrs(graph_dict, start_station, goal_station)

print("Fewest Stops Path:", path)
print("Total Stops:", stops)