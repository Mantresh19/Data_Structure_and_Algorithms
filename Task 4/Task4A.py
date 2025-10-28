import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
libraries_path = os.path.join(base_dir, "Libraries")
sys.path.insert(0, libraries_path)

from mst import kruskal, get_total_weight, print_undirected_edges
from adjacency_list_graph import AdjacencyListGraph
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
G = AdjacencyListGraph(len(stations), False, True)
for u, v, w in edges:
    G.insert_edge(stations.index(u), stations.index(v), w)
print("Original network:")
print(G.strmap(lambda i: stations[i]))
print()
mst_graph = kruskal(G)
print("Core Network Backbone (Minimum Spanning Tree via Kruskal):")
print_undirected_edges(mst_graph, stations)
total_weight = get_total_weight(mst_graph)
print("\nTotal journey time of core network backbone = ", total_weight)
print("\n✓ Compare the above edges and total weight with your manual trace to verify correctness.")