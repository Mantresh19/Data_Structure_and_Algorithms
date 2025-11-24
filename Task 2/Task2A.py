import os, sys

# Load CLRS Library
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
libraries_path = os.path.join(base_dir, "Libraries")

# Add Libraries to the Python path where my Algorithms are saved
sys.path.insert(0, libraries_path)

# Import graph implementation and Dijkstra’s algorithm from custom CLRS library
from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra

# Defining graph edges where each tuple represents an edge: (u, v, w)
# where u = start node, v = end node, w = weight (or travel time)
edges = [
    (0,1,5), (0,2,2), (1,3,1), (2,3,4), (3,4,3)
]
# Create a weighted, undirected graph with 5 vertices (0 to 4)
G = AdjacencyListGraph(5, directed=False, weighted=True)
# Insert all edges into the graph
for u,v,w in edges:
    G.insert_edge(u,v,w)
# Run Dijkstra’s Algorithm
d, pi = dijkstra(G, 0)
# Reconstruct the shortest path
def reconstruct_path(pi, src, dst):
    path = [] # store the final path here
    v = dst # start from destination
    while v is not None:
        path.append(v) # add current node to path
        if v == src: break # base case stop when we reach the source
        v = pi[v] # move to predecessor
    path.reverse() # reverse to get path from source → destination
    return path
# Get the path from vertex 0 (A) to vertex 4 (E)
path = reconstruct_path(pi, 0, 4)
# Optional: give each node a name for readability
names = ["A","B","C","D","E"]
# Convert path of indices [0,2,1,3,4] → ["A","C","B","D","E"]
path_named = [names[i] for i in path]

# Print results
print("Shortest Path:", " → ".join(path_named))
print("Total Journey Time:", d[4], "minutes")

# Verification Check
print()
print("VERIFICATION AGAINST MANUAL CALCULATION")
print()

# Expected results from manual Dijkstra execution
expected_path = [0,2,3,4]  # A→C→B→D→E
expected_time = 9

# Convert expected path to named version for display
expected_path_named = [names[i] for i in expected_path]

print(f"Computed Path:  {path} → {' → '.join(path_named)}")
print(f"Expected Path:  {expected_path} → {' → '.join(expected_path_named)}")
print(f"Path Match:     {path == expected_path}")
print(f"Computed Time:  {d[4]} minutes")
print(f"Expected Time:  {expected_time} minutes")
print(f"Time Match:     {d[4] == expected_time}")
print(f"Full Verification: {path == expected_path and d[4] == expected_time}")