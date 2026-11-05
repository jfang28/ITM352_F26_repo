from pathlib import Path

import pandas as pd


csv_path = Path(__file__).with_name("properties.csv")
properties = pd.read_csv(csv_path)

# Replace "-" placeholders and convert numeric columns stored as text.
for column in ["land_sqft", "gross_sqft", "sale_price"]:
    values = properties[column].astype(str).str.strip()
    properties[column] = pd.to_numeric(
        values.mask(values.str.fullmatch(r"-+")),
        errors="coerce",
    )

# These columns contain labels, so categorical type is appropriate.
properties["borough"] = properties["borough"].astype("category")
properties["neighborhood"] = properties["neighborhood"].astype("category")

large_properties = properties[properties["units"] >= 500].copy()
large_properties = large_properties.drop(
    columns=["id", "block", "lot", "easement"]
)
large_properties = large_properties.dropna().drop_duplicates()
large_properties = large_properties[large_properties["sale_price"] > 0].copy()

print("Cleaned data types:")
print(large_properties.dtypes)
print("\nCleaned data:")
print(large_properties.to_string(index=False))
print("\nAverage sale price:")
print(f"{large_properties['sale_price'].mean():.2f}")