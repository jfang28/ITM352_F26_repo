import pandas as pd
from sodapy import Socrata


client = Socrata("data.cityofchicago.org", None)
results = client.get("rr23-ymwb", limit=500)
vehicles = pd.DataFrame.from_records(results)

print("First few records:")
print(vehicles.head())

print("\nVehicle types and fuel sources:")
print(vehicles[["vehicle_type", "vehicle_fuel_source"]])

print("\nNumber of vehicles per fuel source:")
print(vehicles.groupby("vehicle_fuel_source").size())