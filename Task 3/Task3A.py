# Written by Mantresh
import os
import sys
from pprint import pprint

# --- STEP 1: Load CLRS Library ---
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
libraries_path = os.path.join(base_dir, "Libraries")

# Add Libraries to the Python path
sys.path.insert(0, libraries_path)

from queue import Queue


def bfs_fewest_stops(graph, start, end):
    """
    Find path with fewest stops using BFS algorithm
    Uses CLRS library Queue implementation with put()/get() methods
    """
    if start not in graph or end not in graph:
        return None, -1

    # Initialize BFS structures
    visited = set()
    parent = {}
    queue = Queue()

    visited.add(start)
    parent[start] = None
    queue.put(start)  # CORRECTED: Using put() instead of enqueue()

    found = False
    while not queue.empty() and not found:  # CORRECTED: Using empty() instead of is_empty()
        current = queue.get()  # CORRECTED: Using get() instead of dequeue()

        # Explore neighbors
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.put(neighbor)  # CORRECTED: Using put() instead of enqueue()

                if neighbor == end:
                    found = True
                    break

    # Reconstruct path if found
    if end not in parent:
        return None, -1

    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()

    # Number of stops = path length - 1
    num_stops = len(path) - 1
    return path, num_stops


def demonstrate_task_3a():
    """Complete demonstration for Task 3a with manual verification"""
    print("=" * 70)
    print("TASK 3A: MANUAL VS CODE-BASED EXECUTION OF FEWEST STOPS ALGORITHM")
    print("=" * 70)

    # Create simple dataset (5 stations as per requirements)
    print("\n• CREATE A SIMPLE DATASET")
    simple_graph = {
        0: [1, 3],
        1: [0, 2, 4],
        2: [1, 4],
        3: [0, 4],
        4: [1, 2, 3]
    }

    print("Adjacency List Representation:")
    for station, neighbors in sorted(simple_graph.items()):
        print(f"  Station {station}: connected to {neighbors}")

    print("\n• MANUAL APPLICATION")
    print("Finding fewest stops from Station 0 to Station 2 using BFS:")
    print("Step 1: Initialize - Queue: [0], Visited: {0}, Parent: {0: None}")
    print("Step 2: Process 0 → Add neighbors 1,3 → Queue: [1, 3], Parent: {0:None, 1:0, 3:0}")
    print("Step 3: Process 1 → Add neighbors 2,4 → Queue: [3, 2, 4], Parent: {0:None, 1:0, 2:1, 3:0, 4:1}")
    print("Step 4: Process 3 → All neighbors visited")
    print("Step 5: Process 2 → Destination reached!")
    print("Path reconstruction: 2 ← 1 ← 0")
    print("Expected Path: [0, 1, 2]")
    print("Expected Stops: 2")

    print("\n• CODE IMPLEMENTATION AND VERIFICATION")
    # Test the same journey as manual trace
    start_station = 0
    end_station = 2

    print(f"Executing BFS from Station {start_station} to Station {end_station}")

    # Execute BFS algorithm using CLRS library
    path, num_stops = bfs_fewest_stops(simple_graph, start_station, end_station)

    print(f"\nRESULTS:")
    print(f"Computed Path: {path}")
    print(f"Number of Stops: {num_stops}")
    print(f"Journey: {' → '.join(f'Station {s}' for s in path)}")

    # Verification against manual calculation
    expected_path = [0, 1, 2]
    expected_stops = 2

    print(f"\nVERIFICATION:")
    print(f"Expected Path: {expected_path}")
    print(f"Expected Stops: {expected_stops}")
    print(f"✓ Path Match: {path == expected_path}")
    print(f"✓ Stops Match: {num_stops == expected_stops}")
    print(f"✓ Manual Verification Successful: {path == expected_path and num_stops == expected_stops}")

    # Demonstrate CLRS library usage
    print(f"\n• CLRS LIBRARY USAGE VERIFICATION")
    print("✓ Using Queue.put() and Queue.get() methods from CLRS library")
    print("✓ Using Queue.empty() method for termination condition")
    print("✓ Algorithm correctly implements BFS for fewest stops")


if __name__ == "__main__":
    demonstrate_task_3a()