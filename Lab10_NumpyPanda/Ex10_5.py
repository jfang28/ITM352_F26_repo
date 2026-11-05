from pathlib import Path

import pandas as pd


csv_path = Path(__file__).with_name("properties.csv")
properties = pd.read_csv(csv_path)

large_properties = properties[properties["units"] >= 500].copy()
large_properties = large_properties.drop(
    columns=["id", "block", "lot", "easement"]
)

print(large_properties.head(10))