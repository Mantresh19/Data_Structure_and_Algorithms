import os
import sys

# Setup path to CLRS library
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
libraries_path = os.path.join(base_dir, "Libraries")
sys.path.insert(0, libraries_path)

# Import CLRS MST functions
from mst import kruskal, get_total_weight, print_undirected_edges
from adjacency_list_graph import AdjacencyListGraph

# Simple dataset: 5 stations with weighted connections
stations = ['A', 'B', 'C', 'D', 'E']
edges = [
    ('A', 'B', 4),
    ('A', 'C', 2),
    ('B', 'C', 5),
    ('B', 'D', 10),
    ('C', 'D', 3),
    ('C', 'E', 8),
    ('D', 'E', 7)
]

# Build undirected weighted graph
G = AdjacencyListGraph(len(stations), False, True)
for u, v, w in edges:
    G.insert_edge(stations.index(u), stations.index(v), w)

# Display original network
print("Original network:")
print(G.strmap(lambda i: stations[i]))
print()

# Apply Kruskal's algorithm to find MST
mst_graph = kruskal(G)

# Display MST (core backbone)
print("Core Network Backbone (Minimum Spanning Tree via Kruskal):")
print_undirected_edges(mst_graph, stations)

# Calculate total weight
total_weight = get_total_weight(mst_graph)
print(f"\nTotal journey time of core network backbone = {total_weight}")

print("\n✓ Compare the above edges and total weight with your manual trace to verify correctness.")