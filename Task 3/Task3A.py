# Import Libraries To Python Path
import os, sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
libraries_path = os.path.join(base_dir, "Libraries")

sys.path.insert(0, libraries_path)

from clrsPython import bfs
from collections import defaultdict
# Define a simple undirected graph using adjacency lists
graph = defaultdict(list)
graph['A'] = ['B'] # Only connected to B
graph['B'] = ['A', 'C'] # Connects to A and C
graph['C'] = ['B', 'D'] # Connects to B and D
graph['D'] = ['C', 'E'] # Connects to C and E
graph['E'] = ['D'] # End station

# Find the path with the fewest stops between two stations using Breadth-First Search (BFS)
def fewest_stops_path_bfs(graph, start, goal):
    # Initialize all stations as unvisited
    visited = {station: False for station in graph}
    # Dictionary to keep track of each station’s parent (for path reconstruction)
    parent = {station: None for station in graph}
    # Queue to manage BFS traversal
    queue = []

    # Start BFS from the starting station
    queue.append(start)
    visited[start] = True

    # BFS Traversal
    while queue:
        current = queue.pop(0) # Dequeue the first station
        if current == goal:
            break # Stop when the goal is reached
        # Explore all connected stations (neighbors)
        for neighbor in graph[current]:
            if not visited[neighbor]:
                visited[neighbor] = True
                parent[neighbor] = current # Record how we reached this neighbor
                queue.append(neighbor) # Enqueue for further exploration

    # Reconstruct path
    path = []
    current = goal
    while current is not None:
        path.insert(0, current) # Insert each station at the front
        current = parent[current] # Move to the parent

    # Validate and return the result
    if path[0] == start:
        total_stops = len(path) - 1 # Total stops = edges in the path
        return path, total_stops
    else:
        # If the start station is not connected to the goal
        return None, None


# Test the dataset
start_station = 'A'
goal_station = 'E'

# Run the BFS function to find the fewest-stop route
path, total_stops = fewest_stops_path_bfs(graph, start_station, goal_station)

# Display the results
print("Fewest Stops Path:", path)
print("Total Number of Stops:", total_stops)