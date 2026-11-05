from pathlib import Path

import pandas as pd


json_path = Path(__file__).with_name("Taxi_Trips.json")
taxi_trips = pd.read_json(json_path)

print(taxi_trips)
print("\nSummary statistics:")
print(taxi_trips.describe())
print("\nMedian:")
print(taxi_trips["fare"].median())