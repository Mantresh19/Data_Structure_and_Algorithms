import os, sys, random, time
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# ============================================================
# IMPORT CLRS LIBRARY (MANDATORY)
# ============================================================
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
libraries_path = os.path.join(base_dir, "Libraries", "clrsPython")
sys.path.insert(0, libraries_path)

from adjacency_list_graph import AdjacencyListGraph
from bfs import bfs


# ============================================================
# REUSE 3(a) APPROACH: Build CLRS Graph from adjacency dict
# ============================================================
def build_clrs_graph_from_dict(graph_dict, name_to_id):
    n = len(name_to_id)
    G = AdjacencyListGraph(n, directed=False, weighted=False)

    for u in graph_dict:
        u_id = name_to_id[u]
        for v in graph_dict[u]:
            v_id = name_to_id[v]

            # Skip any self-loop (CLRS cannot accept)
            if u_id == v_id:
                continue

            # Insert edge if it does not already exist
            if not G.has_edge(u_id, v_id):
                G.insert_edge(u_id, v_id)

    return G


# ============================================================
# REUSE BFS Fewest-stops method from 3(a)
# Now using CLRS BFS ONLY
# ============================================================
def fewest_stops_path_clrs(graph_dict, start, goal):
    stations = list(graph_dict.keys())
    name_to_id = {name: idx for idx, name in enumerate(stations)}
    id_to_name = {idx: name for name, idx in name_to_id.items()}

    G = build_clrs_graph_from_dict(graph_dict, name_to_id)

    start_id = name_to_id[start]
    goal_id = name_to_id[goal]

    dist, pi = bfs(G, start_id)

    # reconstruct path using CLRS predecessor array
    path_ids = []
    current = goal_id
    while current is not None:
        path_ids.insert(0, current)
        current = pi[current]

    if path_ids[0] != start_id:
        return None, None  # unreachable

    path_names = [id_to_name[i] for i in path_ids]
    stops = len(path_ids) - 1
    return path_names, stops


# ============================================================
# PART 1 — EMPIRICAL PERFORMANCE MEASUREMENT (3b)
# ============================================================

# Generate artificial networks in CLRS-compatible form
def generate_artificial_graph_dict(n):
    """
    Creates adjacency dict: 0..n-1 with random undirected edges.
    Compatible with CLRS BFS (integer nodes).
    """
    graph = {i: [] for i in range(n)}
    for i in range(n):
        # connect node i with up to 3 random others
        neighbours = random.sample(range(n), k=min(3, n - 1))
        for j in neighbours:
            if j != i and j not in graph[i]:
                graph[i].append(j)
                graph[j].append(i)
    return graph


# Timing test
sizes = [100, 200, 400, 600, 800, 1000]
avg_times = []

print("\n=== Empirical Measurement for BFS Fewest Stops ===")

for n in sizes:
    graph_dict = generate_artificial_graph_dict(n)

    # convert keys to strings so fewest_stops_path_clrs works with its mapping
    graph_dict_named = {str(k): [str(v) for v in graph_dict[k]] for k in graph_dict}

    pairs = [(str(random.randint(0, n - 1)),
              str(random.randint(0, n - 1)))
             for _ in range(10)]

    total = 0
    for s, g in pairs:
        start_t = time.time()
        fewest_stops_path_clrs(graph_dict_named, s, g)
        total += time.time() - start_t

    avg = total / len(pairs)
    avg_times.append(avg)
    print(f"n={n} → avg BFS time = {avg:.6f}s")


# Plot results
plt.figure(figsize=(8, 5))
plt.plot(sizes, avg_times, marker='o')
plt.title("Average BFS Time vs Network Size (Fewest Stops)")
plt.xlabel("Number of Stations (n)")
plt.ylabel("Average Time (seconds)")
plt.grid(True)
plt.show()


# ============================================================
# PART 2 — APPLICATION WITH LONDON UNDERGROUND DATA
# ============================================================
print("\n=== Application with London Underground Data ===")

data_path = os.path.join(base_dir, "data.csv")
df = pd.read_csv(data_path)

# Assume first 2 columns are station pairs
col1, col2 = df.columns[:2]

graph_real = defaultdict(list)
for _, row in df.iterrows():
    # Station names can be NaN → convert safely
    a = str(row[col1]).strip()
    b = str(row[col2]).strip()

    # Skip invalid or NaN entries
    if a == "" or b == "" or a.lower() == "nan" or b.lower() == "nan":
        continue

    graph_real[a].append(b)
    graph_real[b].append(a)
# Example 1
p1, s1 = fewest_stops_path_clrs(graph_real, "Covent Garden", "Leicester Square")
print("\nJourney 1: Covent Garden → Leicester Square")
print("Path:", p1)
print("Stops:", s1)

# Example 2
p2, s2 = fewest_stops_path_clrs(graph_real, "Wimbledon", "Stratford")
print("\nJourney 2: Wimbledon → Stratford")
print("Path:", p2)
print("Stops:", s2)