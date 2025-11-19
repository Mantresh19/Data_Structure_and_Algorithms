import random, time
import pandas as pd
from collections import defaultdict
import os, sys

# Determine project directory so we can import custom libraries
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
libraries_path = os.path.join(base_dir, "Libraries")
sys.path.insert(0, libraries_path)

from clrsPython import bfs  # mandatory library

# REUSE FUNCTION FROM TASK 3(a)
# Breadth-First Search to compute the fewest-stops path between stations
def fewest_stops_path_bfs(graph, start, goal):
    # Track visited stations to avoid revisiting
    visited = {station: False for station in graph}
    # Parent map to reconstruct the final path
    parent = {station: None for station in graph}
    # BFS queue
    queue = []

    # BFS search loop
    queue.append(start)
    visited[start] = True

    while queue:
        current = queue.pop(0)
        # Stop when goal found
        if current == goal:
            break
        # Explore neighbours
        for neighbor in graph[current]:
            if not visited[neighbor]:
                visited[neighbor] = True
                parent[neighbor] = current
                queue.append(neighbor)

    # reconstruct path
    path = []
    current = goal
    while current is not None:
        path.insert(0, current)
        current = parent[current]

    # Return valid path and number of stops
    if path[0] == start:
        return path, len(path) - 1
    else:
        return None, None


# Generate artificial networks of size n
def generate_artificial_network(n):
    graph = defaultdict(list)
    for i in range(n):
        # Each node connects to up to 3 random others
        connections = random.sample(range(n), k=min(3, n-1))
        for j in connections:
            if i != j:
                graph[i].append(j)
                graph[j].append(i)
    return graph


# Empirical timing
import matplotlib.pyplot as plt
# Network sizes to test
sizes = [100, 200, 400, 600, 800, 1000] # Store average BFS runtimes
avg_times = []

for n in sizes:
    graph = generate_artificial_network(n)
    # Choose 10 random start–goal pairs
    pairs = [(random.randint(0, n-1), random.randint(0, n-1)) for _ in range(10)]
    total_time = 0
    for s, g in pairs:
        start_time = time.time()
        fewest_stops_path_bfs(graph, s, g)
        total_time += (time.time() - start_time)
    # Average BFS time for this network size
    avg_times.append(total_time / len(pairs))

# Plot runtime vs graph size
plt.plot(sizes, avg_times, marker='o')
plt.title('Average BFS Time vs Network Size (Fewest Stops)')
plt.xlabel('Number of Stations (n)')
plt.ylabel('Average Time (seconds)')
plt.grid(True)
plt.show()


# Load real London Underground network data
# Assumes a CSV file with columns: From, To (station names)
data_path = os.path.join(base_dir, "data.csv")  # ✅ or data.xlsx if you converted it
df = pd.read_csv(data_path)

# Assume columns: From, To (ignore journey time since we count stops)
graph = defaultdict(list)
for _, row in df.iterrows():
    station1, station2 = row.iloc[0], row.iloc[1]
    graph[station1].append(station2)
    graph[station2].append(station1)

# Example 1: Covent Garden to Leicester Square
path1, stops1 = fewest_stops_path_bfs(graph, "Covent Garden", "Leicester Square")
print("\nJourney 1:")
print("Path:", path1)
print("Number of Stops:", stops1)

# Example 2: Wimbledon to Stratford
path2, stops2 = fewest_stops_path_bfs(graph, "Wimbledon", "Stratford")
print("\nJourney 2:")
print("Path:", path2)
print("Number of Stops:", stops2)