import sys
import os
import pandas as pd

# Path for the Libraries folder
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
libraries_path = os.path.join(base_dir, "Libraries")

sys.path.insert(0, libraries_path)

# Import Algorithms (CLRS Library)
from chained_hashtable import ChainedHashTable
from dll_sentinel import DLLSentinel

# 1. SMALL ARTIFICIAL DATASET (5 STATIONS)
print("Simple Dataset Example (A–E)")
stations_simple = ['A', 'B', 'C', 'D', 'E']
ht_small = ChainedHashTable(8)  # small table with 8 buckets
# Insert stations one by one and print internal state
for s in stations_simple:
    ht_small.insert(s)
    print(f"After inserting {s}: {ht_small}")

# Status check for station 'C'
query_station = 'C'
status = "Operational" if ht_small.search(query_station) else "Not Found"
print(f"\nStatus check for '{query_station}': {status}")

# 2. USING REAL LONDON UNDERGROUND DATA
print("\nUsing London Underground Data.xlsx")
# Load Excel file
import os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(base_dir, "data.csv")
df = pd.read_csv(file_path)

# Automatically pick the first text-like column
station_col = None
for col in df.columns:
    if df[col].dtype == object:
        station_col = col
        break

# Extract unique station names, clean formatting
stations = df[station_col].astype(str).str.strip().dropna().unique().tolist()
stations = [s for s in stations if s and not s.lower().startswith('nan')]

print(f"Total stations loaded: {len(stations)}")

# Build hashtable with all station names (lowercased for uniformity)
ht_london = ChainedHashTable(len(stations) * 2)
for s in stations:
    ht_london.insert(s.lower())

# Perform example queries
queries = ['Victoria', 'Paddinton', 'NotARealStation']
for q in queries:
    result = "Operational" if ht_london.search(q.lower()) else "Not Found"
    print(f"Query: '{q}' → {result}")

print("\n=== End of Task 1(a) ===")