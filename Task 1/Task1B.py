import sys
import os
import pandas as pd
import random
import time
import matplotlib.pyplot as plt

# Dynamically build the path to the Libraries folder
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
libraries_path = os.path.join(base_dir, "Libraries")

# Add Libraries to the Python path
sys.path.insert(0, libraries_path)

from chained_hashtable import ChainedHashTable
from dll_sentinel import DLLSentinel

# 1. EMPIRICAL PERFORMANCE MEASUREMENT

print("\nEmpirical Performance Measurement")

sizes = [1000, 5000, 10000, 25000, 50000]
queries_per_test = 10000
avg_times = []

for n in sizes:
    ht = ChainedHashTable(n)
    # Insert n unique integers (simulating station IDs)
    for i in range(n):
        ht.insert(i)

    # Time Measurement
    # queries_per_test = 10000
    queries = [random.randint(0, int(n * 1.2)) for _ in range(queries_per_test)]

    # Warm-up run
    for q in queries[:100]:
        _ = ht.search(q)

    # Measure average search time
    t0 = time.perf_counter()
    for q in queries:
        _ = ht.search(q)
    t1 = time.perf_counter()

    avg_time = (t1 - t0) / queries_per_test
    avg_times.append(avg_time)

    print(f"n={n:6d} → Average time per membership check: {avg_time:.8e} s")

# Plot results
plt.figure(figsize=(8, 5))
plt.plot(sizes, avg_times, marker='o', linestyle='-')
plt.xlabel("Dataset size (n)")
plt.ylabel("Average time per membership check (seconds)")
plt.title("Empirical Performance of CLRS Chained Hash Table")
plt.grid(True)

# Save figure beside your data for report use
plot_path = os.path.join(base_dir, "membership_time_plot_clrs.png")
plt.savefig(plot_path)
plt.show()

print(f"\nPerformance plot saved to: {plot_path}")

# 2. APPLICATION WITH LONDON UNDERGROUND DATA

print("\nApplication with London Underground Data")

# Load CSV or Excel file
data_path = os.path.join(base_dir, "data.csv")
df = pd.read_csv(data_path)

# Automatically detect first string-type column
station_col = None
for col in df.columns:
    if df[col].dtype == object:
        station_col = col
        break

# Extract & clean station names
stations = df[station_col].astype(str).str.strip().dropna().unique().tolist()
stations = [s for s in stations if s and not s.lower().startswith('nan')]
print(f"Total stations loaded: {len(stations)}")

# Build Hash Table with all station names (lowercase for consistency)
ht_london = ChainedHashTable(len(stations) * 2)
for s in stations:
    ht_london.insert(s.lower())

# Test a few lookups (presence + absence)
queries = ['Victoria', 'Paddinton', 'NotARealStation']
for q in queries:
    status = "Operational" if ht_london.search(q.lower()) else "Not Found"
    print(f"Query: '{q}' → {status}")