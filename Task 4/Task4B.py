import pandas as pd
import time
import matplotlib.pyplot as plt
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
libraries_path = os.path.join(base_dir, "Libraries")
sys.path.insert(0, libraries_path)

from generate_random_graph import generate_random_graph
from mst import kruskal,get_total_weight, print_undirected_edges
from adjacency_list_graph import AdjacencyListGraph
def measure_mst_times():
    sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    avg_times = []
    for n in sizes:
        G = generate_random_graph(n, 0.015, True, False, True, 1, 14)
        runs = 6
        total_time = 0
        for _ in range(runs):
            start = time.perf_counter()
            kruskal(G)
            end = time.perf_counter()
            total_time += (end - start)
        avg_time = total_time / runs
        avg_times.append(avg_time)
        print(f"n={n} → average time: {avg_time:} seconds")
    return sizes, avg_times
def plot_results(sizes, avg_times):
    plt.figure(figsize=(10, 11))
    plt.plot(sizes, avg_times, marker='o', linestyle='-', color='b', label="runtime")
    for i, txt in enumerate(avg_times):
        plt.text(sizes[i], avg_times[i] + 0.0005, f"{txt:.4f}", ha='center', fontsize=8)
    plt.xlabel("number of stations")
    plt.ylabel("average time seconds")
    plt.title("kruskal performance")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    sizes, avg_times = measure_mst_times()
    plot_results(sizes, avg_times)
FILEPATH = os.path.join(base_dir, "data.csv")
df = pd.read_csv(FILEPATH, header=None, skiprows=1, usecols=[1, 2, 3])
df.columns = ["StationA", "StationB", "Time"]
df = df.dropna(subset=["StationA", "StationB", "Time"])
df["StationA"] = df["StationA"].astype(str).str.strip()
df["StationB"] = df["StationB"].astype(str).str.strip()
df["Time"] = pd.to_numeric(df["Time"], errors="coerce")
df = df[df["Time"].notna()]
edge_map = {}
for a, b, w in zip(df["StationA"], df["StationB"], df["Time"]):
    key = (a, b) if a <= b else (b, a)
    w = float(w)
    if key not in edge_map or w < edge_map[key]:
        edge_map[key] = w

edges = [(a, b, w) for (a, b), w in edge_map.items()]


stations = sorted({u for u, v, _ in edges} | {v for u, v, _ in edges})
idx = {name: i for i, name in enumerate(stations)}
G = AdjacencyListGraph(len(stations), False, True)
for u_name, v_name, w in edges:
    u, v = idx[u_name], idx[v_name]
    if u != v:
        G.insert_edge(u, v, float(w))
mst_graph = kruskal(G)
total_weight = get_total_weight(mst_graph)
print("Core Network Backbone (Minimum Spanning Tree via Kruskal):")
print_undirected_edges(mst_graph, stations,)
print("\nTotal journey time of core network backbone =", total_weight, "minutes")
# closables
orig_edges = {(min(idx[a], idx[b]), max(idx[a], idx[b])) for a, b, _ in edges}
mst_edges = set()
for u in range(mst_graph.get_card_V()):
    for e in mst_graph.get_adj_list(u):
        v = e.get_v()
        if u < v:
            mst_edges.add((u, v))
closable_edges = orig_edges - mst_edges
print(f'number of closables edges:{len(closable_edges)} Examples:',end=',')
for (u, v) in list(closable_edges)[:10]:
    print(f"({stations[u]} - {stations[v]})",end=',')