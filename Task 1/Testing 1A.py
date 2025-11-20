"""
TASK 1(a) - Operational Station Status System
Using CLRS Chained Hash Table Library
This script demonstrates manual vs code-based execution for hash table operations
"""

import sys
import os
import pandas as pd

# ============================================================================
# SETUP: Path configuration for CLRS library
# ============================================================================
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
libraries_path = os.path.join(base_dir, "Libraries")
sys.path.insert(0, libraries_path)

# Import CLRS algorithms
from chained_hashtable import ChainedHashTable
from dll_sentinel import DLLSentinel


# ============================================================================
# HELPER FUNCTION: Visualize hash table internal state
# ============================================================================
def print_hashtable_state(ht, step_name):
    """
    Print the internal bucket structure of a chained hash table.
    This helps create the manual trace visualization for the report.

    Args:
        ht: ChainedHashTable instance
        step_name: Description of current step (e.g., "After inserting A")
    """
    print(f"\n{'='*60}")
    print(f"{step_name}")
    print(f"{'='*60}")

    for i in range(ht.m):  # m is the number of buckets
        bucket_items = []
        # Navigate through the doubly-linked list in each bucket
        try:
            node = ht.table[i].head.next
            while node != ht.table[i].head:
                bucket_items.append(str(node.key))
                node = node.next
        except:
            pass

        if bucket_items:
            print(f"  Bucket {i}: {' -> '.join(bucket_items)}")
        else:
            print(f"  Bucket {i}: [empty]")
    print(f"{'='*60}\n")


# ============================================================================
# PART 1: SIMPLE ARTIFICIAL DATASET (5 STATIONS)
# ============================================================================
print("\n" + "="*70)
print("TASK 1(a): DATA STRUCTURE SELECTION - CHAINED HASH TABLE")
print("="*70)
print("\nJustification:")
print("  - Insertion: O(1) average time")
print("  - Deletion: O(1) average time")
print("  - Membership check: O(1) average time")
print("  - Suitable for frequent updates and fast status checks\n")

print("\n" + "="*70)
print("SIMPLE DATASET: Manual Trace with 5 Stations (A, B, C, D, E)")
print("="*70)

# Create small dataset
stations_simple = ['A', 'B', 'C', 'D', 'E']
ht_small = ChainedHashTable(8)  # 8 buckets for clear visualization

print("\nInitial State: Empty hash table with 8 buckets")
print_hashtable_state(ht_small, "Initial State (Empty)")

# Insert stations one by one, showing state after each insertion
for idx, station in enumerate(stations_simple, 1):
    ht_small.insert(station)
    print_hashtable_state(ht_small, f"Step {idx}: After inserting '{station}'")

# ============================================================================
# MANUAL APPLICATION: Status check demonstration
# ============================================================================
print("\n" + "="*70)
print("MANUAL APPLICATION: Status Check for Station 'C'")
print("="*70)

query_station = 'C'
result = ht_small.search(query_station)
status = "Operational" if result else "Not Found"

print(f"\nQuery: '{query_station}'")
print(f"Result: {status}")
print(f"Details: Station '{query_station}' {'exists' if result else 'does not exist'} in the operational list")


# ============================================================================
# PART 2: CODE IMPLEMENTATION WITH LONDON UNDERGROUND DATA
# ============================================================================
print("\n\n" + "="*70)
print("APPLICATION WITH LONDON UNDERGROUND DATA")
print("="*70)

# Data acquisition
data_path = os.path.join(base_dir, "data.csv")

try:
    df = pd.read_csv(data_path)
    print(f"\n✓ Successfully loaded data from: {data_path}")

    # Automatically detect first string-type column (station names)
    station_col = None
    for col in df.columns:
        if df[col].dtype == object:
            station_col = col
            break

    if station_col is None:
        raise ValueError("No text column found in CSV")

    print(f"✓ Detected station column: '{station_col}'")

    # Extract unique station names and clean formatting
    stations = df[station_col].astype(str).str.strip().dropna().unique().tolist()
    stations = [s for s in stations if s and not s.lower().startswith('nan')]

    print(f"✓ Total unique stations loaded: {len(stations)}")

    # Build hash table with all station names
    # Table size = 2 * num_stations for good load factor (α ≈ 0.5)
    table_size = len(stations) * 2
    ht_london = ChainedHashTable(table_size)

    print(f"✓ Created hash table with {table_size} buckets")
    print(f"✓ Load factor α ≈ {len(stations)/table_size:.2f}")

    # Insert all stations (lowercase for case-insensitive lookup)
    for station in stations:
        ht_london.insert(station.lower())

    print(f"✓ Inserted {len(stations)} stations into hash table\n")

    # ============================================================================
    # TESTING: Demonstrate presence and absence checks
    # ============================================================================
    print("\n" + "="*70)
    print("TESTING: Status Checks on Real Network")
    print("="*70)
    print("\nPerforming three test queries:")
    print("  1. Valid station (exact spelling)")
    print("  2. Invalid station (misspelled)")
    print("  3. Invalid station (fictional)\n")

    test_queries = [
        ('Victoria', 'Valid station - should be found'),
        ('Paddinton', 'Misspelled "Paddington" - should NOT be found'),
        ('NotARealStation', 'Fictional station - should NOT be found')
    ]

    for query, description in test_queries:
        result = ht_london.search(query.lower())
        status = "✓ Operational" if result else "✗ Not Found"

        print(f"\n{'─'*70}")
        print(f"Query: '{query}'")
        print(f"Description: {description}")
        print(f"Status: {status}")
        print(f"{'─'*70}")

    print("\n\n" + "="*70)
    print("TASK 1(a) COMPLETED SUCCESSFULLY")
    print("="*70)
    print("\n⚠ REPORT NOTE: Take screenshots of the above output for your report")
    print("   Required screenshots:")
    print("   1. Manual trace showing hash table state after each insertion")
    print("   2. Status check results for all three test queries")

except FileNotFoundError:
    print(f"\n✗ ERROR: Could not find data file at {data_path}")
    print("  Please ensure 'data.csv' is in the correct location")
except Exception as e:
    print(f"\n✗ ERROR: {str(e)}")
    print("  Please check your data file format and library installation")

print("\n" + "="*70)
print("END OF TASK 1(a)")
print("="*70 + "\n")