import pandas as pd
import requests


url = (
    "https://data.cityofchicago.org/resource/97wa-y6ff.json"
    "?$select=driver_type,count(license)&$group=driver_type"
)
response = requests.get(url)
response.raise_for_status()
records = response.json()

print("Response records (a list of dictionaries):")
print(records)

licenses = pd.DataFrame.from_records(records).rename(
    columns={"count_license": "count"}
)
licenses = licenses[["count", "driver_type"]].set_index("driver_type")

print("\nLicense counts by driver type:")
print(licenses)