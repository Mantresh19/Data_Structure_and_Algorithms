import os, sys, time, random
import pandas as pd
import matplotlib.pyplot as plt

# Load CLRS Library
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
libraries_path = os.path.join(base_dir, "Libraries")

# Add Libraries to the Python path
sys.path.insert(0, libraries_path)

from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra


# Reconstruct shortest path from predecessor list
def reconstruct_path(pi, src, dst):
    path = []
    v = dst
    while v is not None:
        path.append(v)
        if v == src:
            break
        v = pi[v]
    path.reverse()
    return path


# Generate Random Graph
def generate_random_graph(AdjacencyListGraph, n, p=0.03, wmin=1, wmax=10):
    """Creates a connected random graph with ~p density."""
    G = AdjacencyListGraph(n, directed=False, weighted=True)
    # Ensure connectivity with a simple chain
    for i in range(n - 1):
        G.insert_edge(i, i + 1, random.randint(wmin, wmax))
    # Add extra random edges
    for i in range(n):
        for j in range(i + 2, n):
            if random.random() < p:
                G.insert_edge(i, j, random.randint(wmin, wmax))
    return G


# Empirical Performance Measurement
def benchmark_dijkstra(sizes=(100,200,400,600,800,1000), trials=100):
    """Measures average execution time of Dijkstra’s algorithm."""
    results = []
    for n in sizes:
        G = generate_random_graph(AdjacencyListGraph, n)
        pairs = [(random.randrange(n), random.randrange(n)) for _ in range(trials)]
        t0 = time.perf_counter()
        for s, t in pairs:
            if s != t:
                dijkstra(G, s)
        t1 = time.perf_counter()
        avg_time = (t1 - t0) / trials
        results.append((n, avg_time))
        print(f"n={n:4d} → average time per shortest-path: {avg_time:.6f}s")
    return results


# Plot Results
def plot_results(results):
    x = [n for n,_ in results]
    y = [t for _,t in results]
    plt.plot(x, y, marker="o")
    plt.xlabel("Network size n (stations)")
    plt.ylabel("Average time per shortest-path (s)")
    plt.title("Empirical Performance of Dijkstra’s Algorithm")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.savefig("avg_time_vs_n.png", dpi=200)
    plt.show()


# Apply to London Underground Data (CSV)
def apply_to_london():
    """Builds a real tube network and finds shortest journeys."""
    data_path = os.path.join(base_dir, "data.csv")  # ✅ updated path
    df = pd.read_csv(data_path)

    # Extract and clean data
    colA, colB, colT = df.columns[1], df.columns[2], df.columns[3]
    df = df[[colA, colB, colT]].dropna()
    df = df[df[colT].apply(lambda x: isinstance(x,(int,float)))]

    # Keep minimum time between duplicate stations
    key_min = {}
    for a, b, t in zip(df[colA], df[colB], df[colT]):
        key = tuple(sorted((str(a).strip(), str(b).strip())))
        key_min[key] = min(float(t), key_min.get(key, float("inf")))
    edges = [(a,b,t) for (a,b),t in key_min.items()]

    # Build graph
    stations = sorted({a for a,_,_ in edges} | {b for _,b,_ in edges})
    name_to_id = {n:i for i,n in enumerate(stations)}
    id_to_name = {i:n for n,i in name_to_id.items()}
    G = AdjacencyListGraph(len(stations), directed=False, weighted=True)
    for a,b,t in edges:
        G.insert_edge(name_to_id[a], name_to_id[b], t)

        # Display shortest path
        def shortest_path(src, dst):
            s, t = name_to_id[src], name_to_id[dst]
            d, pi = dijkstra(G, s)
            path_ids = reconstruct_path(pi, s, t)
            names = [id_to_name[i] for i in path_ids]

            print(f"\n{'=' * 60}")
            print(f"Journey: {src} → {dst}")
            print(f"{'=' * 60}")
            print(f"Number of stations: {len(names)}")
            print(f"Total journey time: {d[t]} minutes")
            print(f"\nDetailed Path:")

            # Print each station on a new line with step number
            for idx, station in enumerate(names, 1):
                if idx == 1:
                    print(f"  {idx}. {station} (START)")
                elif idx == len(names):
                    print(f"  {idx}. {station} (END)")
                else:
                    print(f"  {idx}. {station}")
            print(f"{'=' * 60}\n")

    # Example short and long route
    shortest_path("Covent Garden", "Leicester Square")
    shortest_path("Wimbledon", "Stratford")


# Main
if __name__ == "__main__":
    # Measure performance
    results = benchmark_dijkstra()
    plot_results(results)
    # Apply on real dataset
    apply_to_london()
