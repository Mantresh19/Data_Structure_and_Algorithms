import sys
sys.path.append('https://github.com/Mantresh19/clrsPython')
from chained_hashtable import ChainedHashTable
class StationStatusSystem:
    def __init__(self, size=10):
        self.stations = ChainedHashTable(size)  # stores operational stations only
        self.all_stations = ['A', 'B', 'C', 'D', 'E']  # all known stations

    def add_station(self, station_name):
        self.stations.insert(station_name)

    def is_operational(self, station_name):
        # Step 1: Check if station exists at all
        if station_name not in self.all_stations:
            return "Not Found"
        # Step 2: Check if it's operational (present in hash table)
        return "Operational" if self.stations.search(station_name) is not None else "Not Operational"

def task_1a():
    print("=== Task 1a: Station Status System ===\n")
    system = StationStatusSystem(size=10)

    # Only some stations are operational today
    operational_today = ['A', 'C', 'E']
    for s in operational_today:
        system.add_station(s)

    test_stations = ['A', 'D', 'Z']  # A operational, B not operational, Z doesn't exist
    for test in test_stations:
        print(f"\nChecking status for station '{test}':")
        print(f"Station '{test}' is {system.is_operational(test)}")

if __name__ == "__main__":
    task_1a()
