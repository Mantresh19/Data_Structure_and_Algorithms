import os, sys

# Add Libraries path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
libraries_path = os.path.join(base_dir, "Libraries", "clrsPython")
sys.path.insert(0, libraries_path)

from adjacency_list_graph import AdjacencyListGraph
from bfs import bfs

# ================================
# Simple Dataset (5 Stations)
# ================================
graph_dict = {
    'A': ['B'],
    'B': ['A', 'C'],
    'C': ['B', 'D'],
    'D': ['C', 'E'],
    'E': ['D']
}

# Map station names → integers
stations = list(graph_dict.keys())
name_to_id = {name: idx for idx, name in enumerate(stations)}
id_to_name = {idx: name for name, idx in name_to_id.items()}


# ================================
# Build CLRS Graph (undirected)
# ================================
def build_clrs_graph(graph_dict):
    card_V = len(graph_dict)
    G = AdjacencyListGraph(card_V, directed=False, weighted=False)

    for u in graph_dict:
        u_id = name_to_id[u]
        for v in graph_dict[u]:
            v_id = name_to_id[v]
            # insert only if not exists
            if not G.has_edge(u_id, v_id):
                G.insert_edge(u_id, v_id)

    return G


# ================================
# BFS Fewest Stops using CLRS BFS
# ================================
def fewest_stops_path_clrs(graph_dict, start, goal):
    G = build_clrs_graph(graph_dict)

    start_id = name_to_id[start]
    goal_id = name_to_id[goal]

    # CLRS BFS returns (dist[], pi[])
    dist, pi = bfs(G, start_id)

    # Reconstruct path from parent list
    path_ids = []
    current = goal_id
    while current is not None:
        path_ids.insert(0, current)
        current = pi[current]

    # Check if reachable
    if path_ids[0] != start_id:
        return None, None

    # Convert back to station names
    path_names = [id_to_name[i] for i in path_ids]
    return path_names, len(path_ids) - 1


# ================================
# Test Example
# ================================
start_station = 'A'
goal_station = 'E'

path, stops = fewest_stops_path_clrs(graph_dict, start_station, goal_station)

print("Fewest Stops Path:", path)
print("Total Stops:", stops)