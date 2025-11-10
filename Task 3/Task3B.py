# Written by Mantresh
import time
import random
import matplotlib.pyplot as plt


def generate_unweighted_network(n, connection_probability=0.3):
    """Generate artificial tube network with n stations (unweighted)"""
    graph = {i: [] for i in range(n)}

    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < connection_probability:
                graph[i].append(j)
                graph[j].append(i)

    return graph


def measure_bfs_performance(n, num_tests=100):
    """Measure average BFS execution time for network size n"""
    graph = generate_unweighted_network(n)
    total_time = 0
    successful_tests = 0

    for _ in range(num_tests):
        start = random.randint(0, n - 1)
        end = random.randint(0, n - 1)

        # Ensure start != end for meaningful test
        while start == end:
            end = random.randint(0, n - 1)

        try:
            start_time = time.time()
            path, stops = bfs_fewest_stops(graph, start, end)
            end_time = time.time()

            # Only count if path exists
            if path is not None:
                total_time += (end_time - start_time)
                successful_tests += 1
        except:
            continue

    return total_time / successful_tests if successful_tests > 0 else 0


def performance_analysis():
    """Analyze BFS performance across different network sizes"""
    sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    times = []

    print("\n" + "=" * 60)
    print("EMPIRICAL PERFORMANCE MEASUREMENT")
    print("=" * 60)

    for n in sizes:
        avg_time = measure_bfs_performance(n, num_tests=50)
        times.append(avg_time)
        print(f"Network size {n:4d}: {avg_time:.8f} seconds per calculation")

    return sizes, times


def plot_performance(sizes, times):
    """Plot empirical performance vs theoretical complexity"""
    plt.figure(figsize=(12, 8))

    # Empirical data
    plt.plot(sizes, times, 'go-', linewidth=2, markersize=8, label='Empirical BFS Performance')

    # Theoretical O(V + E) trend line (normalized)
    theoretical_trend = [t * (sizes[-1] / sizes[0]) for t in times]
    plt.plot(sizes, theoretical_trend, 'r--', linewidth=1, label='Theoretical O(V + E) Trend')

    plt.xlabel('Number of Stations (V)')
    plt.ylabel('Average Time per Calculation (seconds)')
    plt.title('BFS Algorithm Performance for Fewest Stops\n(Empirical vs Theoretical O(V + E) Complexity)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('bfs_performance_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()


# Run performance analysis
if __name__ == "__main__":
    sizes, times = performance_analysis()
    plot_performance(sizes, times)