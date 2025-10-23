# ===============================================================
# Task 1(b) - Empirical Measurement and Application
# ===============================================================
# Coursework: COMP1828 - Advanced Algorithms and Data Structures
# Author: [Your Name / Group ID]
# ---------------------------------------------------------------
# Requirements:
#   1. Reuse CLRS ChainedHashTable from Task 1(a)
#   2. Measure empirical performance (membership test)
#   3. Apply system to real London Underground data
# ===============================================================

import sys, time, random
import matplotlib.pyplot as plt
import pandas as pd

# --- Add CLRS library path (adjust only if folder name changes) ----
sys.path.append("/Users/mantresh/Library/CloudStorage/OneDrive-UniversityofGreenwich/Assignment/Year 2/DSA/Coursework/Libraries")

# --- Import hash table from CLRS -----------------------------------
from chained_hashtable import ChainedHashTable

# ===============================================================
# PART 1: EMPIRICAL PERFORMANCE MEASUREMENT
# ===============================================================

def measure_lookup_time(n, num_queries=10000):
    """
    Build a hash table with n unique station IDs (0..n-1),
    then measure average lookup time for random queries.
    """
    ht = ChainedHashTable(m=n*2)   # load factor ~0.5
    for i in range(n):
        ht.insert(str(i))          # store string form for uniformity

    # Generate random query keys (half exist, half don't)
    queries = [str(random.randint(0, n*2)) for _ in range(num_queries)]

    start = time.perf_counter()
    for q in queries:
        ht.search(q)
    end = time.perf_counter()

    avg_time = (end - start) / num_queries
    return avg_time


dataset_sizes = [1000, 5000, 10000, 25000, 50000]
average_times = []

print("=== Measuring Lookup Performance ===")
for n in dataset_sizes:
    avg_t = measure_lookup_time(n)
    average_times.append(avg_t)
    print(f"Dataset size {n}: Average lookup time = {avg_t:.8f} sec")

# --- Plot average lookup time vs dataset size -----------------------
plt.figure(figsize=(7,5))
plt.plot(dataset_sizes, average_times, marker='o')
plt.title("Average Lookup Time vs Dataset Size")
plt.xlabel("Number of Stations (n)")
plt.ylabel("Average Time per Lookup (seconds)")
plt.grid(True)
plt.tight_layout()
plt.savefig("Task1b_Lookup_Performance.png", dpi=200)
plt.show()

# ===============================================================
# PART 2: REAL LONDON UNDERGROUND DATA APPLICATION
# ===============================================================

print("\n=== Building Real Station Status System ===")

# Path to Excel data (update if file moved)
excel_path = "/Users/mantresh/Library/CloudStorage/OneDrive-UniversityofGreenwich/Assignment/Year 2/DSA/Coursework/London Underground data.xlsx"

# --- Load all unique station names from Excel -------------------
df = pd.read_excel(excel_path)
# Assuming columns contain station names in first two columns
station_names = pd.unique(df.iloc[:, :2].values.ravel('K'))
station_names = [str(s).strip() for s in station_names if str(s).strip() != 'nan']

print(f"Total unique stations loaded: {len(station_names)}")

# --- Populate CLRS hash table with all stations -----------------
ht_real = ChainedHashTable(m=len(station_names)*2)
for s in station_names:
    ht_real.insert(s)

# --- Define a helper for status checking -------------------------
def check_station_status(table, station_name):
    found = table.search(station_name)
    status = "Operational" if found is not None else "Not Found"
    print(f"Station: {station_name:20s} → Status: {status}")

# --- Perform 3 example lookups -----------------------------------
print("\n=== Status Checks ===")
check_station_status(ht_real, "Victoria")         # valid
check_station_status(ht_real, "Paddinton")        # misspelled
check_station_status(ht_real, "FictionalStation") # not real

print("\nAll tests complete. Screenshot this section for your report.")
