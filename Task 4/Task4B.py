import pandas as pd
import time
import matplotlib.pyplot as plt
import os
import sys

# Setup path to CLRS library
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
libraries_path = os.path.join(base_dir, "Libraries")
sys.path.insert(0, libraries_path)

# Import CLRS functions
from generate_random_graph import generate_random_graph
from mst import kruskal, get_total_weight, print_undirected_edges
from adjacency_list_graph import AdjacencyListGraph

# PART 1: EMPIRICAL PERFORMANCE MEASUREMENT
def measure_mst_times():
    """Measure average Kruskal execution time for different network sizes"""
    sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    avg_times = []

    for n in sizes:
        # Generate random weighted graph (n stations, ~1.5% edge probability)
        G = generate_random_graph(n, 0.015, True, False, True, 1, 14)

        # Run Kruskal 6 times and average results
        runs = 6
        total_time = 0
        for _ in range(runs):
            start = time.perf_counter()
            kruskal(G)
            end = time.perf_counter()
            total_time += (end - start)

        avg_time = total_time / runs
        avg_times.append(avg_time)
        print(f"n={n} → average time: {avg_time} seconds")

    return sizes, avg_times

def plot_results(sizes, avg_times):
    """Plot performance graph"""
    plt.figure(figsize=(10, 11))
    plt.plot(sizes, avg_times, marker='o', linestyle='-', color='b', label="runtime")

    # Add time labels on points
    for i, txt in enumerate(avg_times):
        plt.text(sizes[i], avg_times[i] + 0.0005, f"{txt:.4f}", ha='center', fontsize=8)

    plt.xlabel("number of stations")
    plt.ylabel("average time (seconds)")
    plt.title("Kruskal's Algorithm Performance")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# Run empirical tests
if __name__ == "__main__":
    sizes, avg_times = measure_mst_times()
    plot_results(sizes, avg_times)

# PART 2: APPLICATION WITH LONDON UNDERGROUND DATA
# Load London Underground data
FILEPATH = os.path.join(base_dir, "data.csv")
df = pd.read_csv(FILEPATH, header=None, skiprows=1, usecols=[1, 2, 3])
df.columns = ["StationA", "StationB", "Time"]

# Clean data: remove NaN, strip whitespace
df = df.dropna(subset=["StationA", "StationB", "Time"])
df["StationA"] = df["StationA"].astype(str).str.strip()
df["StationB"] = df["StationB"].astype(str).str.strip()
df["Time"] = pd.to_numeric(df["Time"], errors="coerce")
df = df[df["Time"].notna()]

# Simplify: keep only minimum time for duplicate connections
edge_map = {}
for a, b, w in zip(df["StationA"], df["StationB"], df["Time"]):
    key = (a, b) if a <= b else (b, a)  # Normalize edge order
    w = float(w)
    if key not in edge_map or w < edge_map[key]:
        edge_map[key] = w

edges = [(a, b, w) for (a, b), w in edge_map.items()]

# Build graph with all unique stations
stations = sorted({u for u, v, _ in edges} | {v for u, v, _ in edges})
idx = {name: i for i, name in enumerate(stations)}  # Map station name to index

G = AdjacencyListGraph(len(stations), False, True)
for u_name, v_name, w in edges:
    u, v = idx[u_name], idx[v_name]
    if u != v:  # Skip self-loops
        G.insert_edge(u, v, float(w))

# Compute MST using Kruskal's algorithm
mst_graph = kruskal(G)

# Display MST results
print("Core Network Backbone (Minimum Spanning Tree via Kruskal):")
print_undirected_edges(mst_graph, stations)

total_weight = get_total_weight(mst_graph)
print(f"\nTotal journey time of core network backbone = {total_weight} minutes")

# IDENTIFY REDUNDANT (CLOSABLE) CONNECTIONS

# Original edges (all connections)
orig_edges = {(min(idx[a], idx[b]), max(idx[a], idx[b])) for a, b, _ in edges}

# MST edges (essential connections)
mst_edges = set()
for u in range(mst_graph.get_card_V()):
    for e in mst_graph.get_adj_list(u):
        v = e.get_v()
        if u < v:  # Only count each edge once (undirected)
            mst_edges.add((u, v))

# Closable edges = original - MST
closable_edges = orig_edges - mst_edges

print(f'\nnumber of closables edges: {len(closable_edges)} Examples:', end='')
for (u, v) in list(closable_edges)[:10]:
    print(f"({stations[u]} - {stations[v]})", end=',')
print()