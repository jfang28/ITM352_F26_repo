import os

import certifi
import pandas as pd

# Python installations on macOS can otherwise use the wrong certificate store.
# certifi supplies the same CA trust while leaving HTTPS verification enabled.
os.environ.setdefault("SSL_CERT_FILE", certifi.where())

# Use the published/raw URL for the CSV provided by the instructor:
SALES_DATA_URL = (
    "https://raw.githubusercontent.com/jfang28/ITM352_F26_repo/main/"
    "Lab10a_PandaPivot/sales_data.csv"
)

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 2000)

try:
    sales_data = pd.read_csv(
        SALES_DATA_URL,
        dtype_backend="pyarrow",
        on_bad_lines="skip",
    )
except (OSError, pd.errors.ParserError) as error:
    print(f"Could not read the URL ({error}); using the local CSV copy.")
    sales_data = pd.read_csv(
        "sales_data.csv",
        dtype_backend="pyarrow",
        on_bad_lines="skip",
    )

print(sales_data.head(5))
print("\nColumn data types:")
print(sales_data.dtypes)
