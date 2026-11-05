import os
from pathlib import Path

import certifi
import numpy as np
import pandas as pd

os.environ.setdefault("SSL_CERT_FILE", certifi.where())

SALES_DATA_URL = (
    "https://raw.githubusercontent.com/jfang28/ITM352_F26_repo/main/"
    "Lab10a_PandaPivot/sales_data.csv"
)
local_file = Path(__file__).with_name("sales_data.csv")

# This controls terminal/DataFrame printing, not creation or filtering.
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 2000)
pd.set_option("display.float_format", "${:,.2f}".format)

try:
    sales_data = pd.read_csv(
        SALES_DATA_URL,
        dtype_backend="pyarrow",
        on_bad_lines="skip",
    )
except (OSError, pd.errors.ParserError) as error:
    print(f"Could not read the URL ({error}); using {local_file.name}.")
    sales_data = pd.read_csv(
        local_file,
        dtype_backend="pyarrow",
        on_bad_lines="skip",
    )

sales_data["order_date"] = pd.to_datetime(
    sales_data["order_date"],
    format="mixed",
    errors="coerce",
)

# Coerce invalid entries to missing numeric values before multiplication.
sales_data["quantity"] = pd.to_numeric(sales_data["quantity"], errors="coerce")
sales_data["unit_price"] = pd.to_numeric(sales_data["unit_price"], errors="coerce")
sales_data["sales"] = sales_data["quantity"] * sales_data["unit_price"]

sales_by_region = pd.pivot_table(
    sales_data,
    values="sales",
    index="sales_region",
    columns="order_type",
    aggfunc=np.sum,
    fill_value=0,
    margins=True,
    margins_name="Total",
)

print("Sales by Region and Order Type:")
print(sales_by_region)
