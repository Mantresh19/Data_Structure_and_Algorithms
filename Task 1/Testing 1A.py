# TASK 1(a) - Operational Station Status System
# Using CLRS Chained Hash Table Library

import sys
import os
import pandas as pd

# ============================================================================
# PATH SETUP FOR CLRS LIBRARY
# ============================================================================
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
libraries_path = os.path.join(base_dir, "Libraries")
sys.path.insert(0, libraries_path)

# Import CLRS algorithms (MANDATORY for coursework compliance)
from chained_hashtable import ChainedHashTable
from dll_sentinel import DLLSentinel

# ============================================================================
# HELPER FUNCTION: VISUALIZE HASH TABLE INTERNAL STATE
# ============================================================================
def print_hashtable_state(ht, step_name="Hash Table State"):
    """
    Prints the internal bucket structure of a ChainedHashTable.
    This is essential for manual trace verification in the report.
    """
    print(f"\n{'='*60}")
    print(f"{step_name}")
    print(f"{'='*60}")
    print(f"Table size (buckets): {ht.m}")
    print(f"Number of elements: {ht.n if hasattr(ht, 'n') else 'N/A'}")
    print(f"\nBucket Contents:")
    print(f"{'-'*60}")

    for i in range(ht.m):
        bucket_items = []
        # Navigate the doubly-linked list in each bucket
        try:
            node = ht.table[i].head.next
            while node != ht.table[i].head:
                bucket_items.append(str(node.key))
                node = node.next
        except:
            pass

        if bucket_items:
            print(f"  Bucket {i:2d}: [{' -> '.join(bucket_items)}]")
        else:
            print(f"  Bucket {i:2d}: [empty]")
    print(f"{'='*60}\n")


# ============================================================================
# PART 1: SIMPLE ARTIFICIAL DATASET (5 STATIONS)
# ============================================================================
print("\n" + "="*70)
print("TASK 1(a): SIMPLE DATASET EXAMPLE")
print("="*70)
print("\nDataset: 5 stations represented as letters A, B, C, D, E")
print("Hash Table Configuration: 8 buckets (to demonstrate collision handling)")

# Create simple dataset
stations_simple = ['A', 'B', 'C', 'D', 'E']

# Initialize hash table with 8 buckets
ht_small = ChainedHashTable(8)

print("\n--- MANUAL TRACE: INSERTION PROCESS ---")
# Insert stations one by one and display internal state after each insertion
for idx, station in enumerate(stations_simple, 1):
    ht_small.insert(station)
    print_hashtable_state(ht_small, f"Step {idx}: After inserting '{station}'")
    input("Press Enter to continue to next insertion...")  # Pause for screenshot

print("\n--- STATUS CHECK DEMONSTRATION ---")
# Perform membership check (as required by the specification)
query_station = 'C'
result = ht_small.search(query_station)
status = "Operational" if result else "Not Found"

print(f"\nQuery: Is station '{query_station}' operational?")
print(f"Result: {status}")
print(f"Technical details: search() returned {result}")

# Additional verification queries
print("\n--- ADDITIONAL VERIFICATION QUERIES ---")
test_queries = ['A', 'E', 'Z']  # Mix of present and absent stations
for q in test_queries:
    result = ht_small.search(q)
    status = "Operational" if result else "Not Found"
    print(f"Query '{q}': {status}")


# ============================================================================
# PART 2: LONDON UNDERGROUND DATA APPLICATION
# ============================================================================
print("\n" + "="*70)
print("LONDON UNDERGROUND DATA APPLICATION")
print("="*70)

# Load the London Underground dataset
data_path = os.path.join(base_dir, "data.csv")
print(f"\nLoading data from: {data_path}")

try:
    df = pd.read_csv(data_path)
    print(f"✓ Data file loaded successfully")
    print(f"  Rows: {len(df)}, Columns: {len(df.columns)}")
except FileNotFoundError:
    print(f"✗ ERROR: File not found at {data_path}")
    print("  Please ensure 'data.csv' is in the project root directory")
    sys.exit(1)

# Automatically detect the station name column (first text column)
station_col = None
for col in df.columns:
    if df[col].dtype == object:  # Object type indicates text/string data
        station_col = col
        break

if not station_col:
    print("✗ ERROR: No text column found for station names")
    sys.exit(1)

print(f"\nDetected station column: '{station_col}'")

# Extract unique station names with robust cleaning
stations_raw = df[station_col].astype(str).str.strip().dropna().unique()
stations = [s.lower() for s in stations_raw if s and not s.lower().startswith('nan')]

print(f"\nData Processing:")
print(f"  Raw unique entries: {len(stations_raw)}")
print(f"  After cleaning: {len(stations)} unique stations")
print(f"  Sample stations: {stations[:5]}")

# Build hash table with appropriate size
# Using 2x stations count to maintain low load factor (α ≈ 0.5)
table_size = len(stations) * 2
ht_london = ChainedHashTable(table_size)

print(f"\nHash Table Configuration:")
print(f"  Number of buckets: {table_size}")
print(f"  Expected load factor: ~{len(stations)/table_size:.2f}")

# Populate hash table
print(f"\nInserting {len(stations)} stations into hash table...")
for station in stations:
    ht_london.insert(station)
print("✓ All stations inserted successfully")

# ============================================================================
# TESTING: PRESENCE AND ABSENCE CHECKS (REQUIRED FOR REPORT)
# ============================================================================
print("\n" + "="*70)
print("TESTING: STATUS CHECKS (Required for Report Screenshots)")
print("="*70)

# Test cases as per specification:
# 1. Valid station (present)
# 2. Misspelled station (absent)
# 3. Fictional station (absent)
test_cases = [
    ('Victoria', 'Valid station - should be Operational'),
    ('Paddinton', 'Misspelled (correct: Paddington) - should be Not Found'),
    ('NotARealStation', 'Fictional station - should be Not Found')
]

print("\n*** PLEASE CAPTURE SCREENSHOTS OF THE FOLLOWING OUTPUT ***\n")

for query, description in test_cases:
    query_lower = query.lower()
    result = ht_london.search(query_lower)
    status = "✓ Operational" if result else "✗ Not Found"

    print(f"Query: '{query}'")
    print(f"  Description: {description}")
    print(f"  Status: {status}")
    print(f"  {'─'*60}")

# Additional test with correct spelling for comparison
print("\nBonus Test - Correct spelling:")
correct_query = 'Paddington'
result = ht_london.search(correct_query.lower())
status = "✓ Operational" if result else "✗ Not Found"
print(f"Query: '{correct_query}'")
print(f"  Status: {status}")

print("\n" + "="*70)
print("END OF TASK 1(a)")
print("="*70)
print("\nREMINDER: Capture screenshots of:")
print("  1. Hash table state after each insertion (simple dataset)")
print("  2. Status check results for all test queries")
print("  3. Include these screenshots in your report")