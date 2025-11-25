import os, sys, random, time
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# IMPORT CLRS LIBRARY
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Path to the local CLRS Python implementation
libraries_path = os.path.join(base_dir, "Libraries", "clrsPython")
# Add CLRS library path to Python import system
sys.path.insert(0, libraries_path)
# Import CLRS-style graph + BFS implementation
from adjacency_list_graph import AdjacencyListGraph
from bfs import bfs

# BUILDING CLRS GRAPH FROM ADJACENCY DICTIONARY
def build_clrs_graph_from_dict(graph_dict, name_to_id):
    n = len(name_to_id)
    G = AdjacencyListGraph(n, directed=False, weighted=False)

    for u in graph_dict:
        u_id = name_to_id[u]
        for v in graph_dict[u]:
            v_id = name_to_id[v]

            # Skip invalid self-loop (CLRS graph does not support)
            if u_id == v_id:
                continue

            # Insert edge if not already present (avoid duplicates)
            if not G.has_edge(u_id, v_id):
                G.insert_edge(u_id, v_id)

    return G


def fewest_stops_path_clrs(graph_dict, start, goal):
    # Create consistent integer ID mapping
    stations = list(graph_dict.keys())
    name_to_id = {name: idx for idx, name in enumerate(stations)}
    id_to_name = {idx: name for name, idx in name_to_id.items()}

    # Build CLRS graph
    G = build_clrs_graph_from_dict(graph_dict, name_to_id)

    # Lookup integer IDs
    start_id = name_to_id[start]
    goal_id = name_to_id[goal]

    # BFS returns (dist[], pi[])
    dist, pi = bfs(G, start_id)

    # Reconstruct path from goal → root using predecessor list
    path_ids = []
    current = goal_id
    while current is not None:
        path_ids.insert(0, current)
        current = pi[current]

    # If root is not the start node → unreachable
    if path_ids[0] != start_id:
        return None, None

    # Convert integer nodes → station names
    path_names = [id_to_name[i] for i in path_ids]
    stops = len(path_ids) - 1

    return path_names, stops

# PART 1 — EMPIRICAL PERFORMANCE MEASUREMENT (3b)
def generate_artificial_graph_dict(n):
    graph = {i: [] for i in range(n)}

    for i in range(n):
        # Choose up to 3 random neighbors (avoid exceeding n-1)
        neighbours = random.sample(range(n), k=min(3, n - 1))
        for j in neighbours:

            # Avoid self-loop and avoid duplicate
            if j != i and j not in graph[i]:
                graph[i].append(j)
                graph[j].append(i)

    return graph

# Prepare test graph sizes
sizes = [100, 200, 400, 600, 800, 1000]
avg_times = []

print("\n=== Empirical Measurement for BFS Fewest Stops ===")

# Loop through each graph size and compute average BFS runtime
for n in sizes:
    # Create random synthetic network
    graph_dict = generate_artificial_graph_dict(n)

    # Convert integer nodes → strings (because fewest_stops_path_clrs expects names)
    graph_dict_named = {str(k): [str(v) for v in graph_dict[k]] for k in graph_dict}

    # Generate 10 random (start, goal) pairs to average runtime
    pairs = [(str(random.randint(0, n - 1)),
              str(random.randint(0, n - 1)))
             for _ in range(10)]

    total = 0
    for s, g in pairs:
        start_t = time.time()
        fewest_stops_path_clrs(graph_dict_named, s, g)
        total += time.time() - start_t

    # Average BFS runtime for this graph size
    avg = total / len(pairs)
    avg_times.append(avg)

    print(f"n={n} → avg BFS time = {avg:.6f}s")

# PLOT PERFORMANCE RESULTS
plt.figure(figsize=(8, 5))
plt.plot(sizes, avg_times, marker='o')
plt.title("Average BFS Time vs Network Size (Fewest Stops)")
plt.xlabel("Number of Stations (n)")
plt.ylabel("Average Time (seconds)")
plt.grid(True)
plt.show()

# PART 2 — APPLICATION WITH REAL LONDON UNDERGROUND DATA
print("\n=== Application with London Underground Data ===")

# Load data.csv (should contain: line, station1, station2)
data_path = os.path.join(base_dir, "data.csv")
df = pd.read_csv(data_path)

# graph_real is adjacency list of station → connected stations
graph_real = defaultdict(list)

# Build the network by parsing each row
for _, row in df.iterrows():

    # Extract line and station names reliably using positional indexing
    line = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
    station1 = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ""
    station2 = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else ""

    # Ensure valid station names (avoid NaNs, blanks, and self-loops)
    if (station1 and station2 and
            station1.lower() != "nan" and station2.lower() != "nan" and
            station1 != station2):

        # Add undirected edge: station1 ↔ station2
        if station2 not in graph_real[station1]:
            graph_real[station1].append(station2)
        if station1 not in graph_real[station2]:
            graph_real[station2].append(station1)

# Remove empty stations and malformed nodes
graph_real = {k: v for k, v in graph_real.items() if k and v}

print(f"Processed {len(graph_real)} stations")
print(f"Sample stations: {list(graph_real.keys())[:10]}")

# EXAMPLE JOURNEYS

# Example 1 — Very close stations
p1, s1 = fewest_stops_path_clrs(graph_real, "Covent Garden", "Leicester Square")
print("\nJourney 1: Covent Garden → Leicester Square")
print("Path:", p1)
print("Stops:", s1)

# Example 2 — Long-distance journey across network
p2, s2 = fewest_stops_path_clrs(graph_real, "Wimbledon", "Stratford")
print("\nJourney 2: Wimbledon → Stratford")
print("Path:", p2)
print("Stops:", s2)