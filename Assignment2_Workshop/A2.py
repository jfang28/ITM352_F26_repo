# Provide secure HTTPS connections and measure loading time.
import ssl
import time
from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen

# Use trusted certificates and pandas to load the sales data.
import certifi
import pandas as pd

# Store the Google Drive CSV address and the columns required by the dashboard.
DRIVE_CSV_URL = "https://drive.google.com/uc?export=download&id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA"
REQUIRED_COLUMNS = {
    "quantity",
    "unit_price",
    "sales_region",
    "order_date",
}


def load_csv(source):
    # Convert a Path object, if needed, to a string so URL parsing works.
    source = str(source)

    # Show which file is being loaded and start a timer for the load operation.
    print(f"Loading CSV file: {source}")
    start_time = time.perf_counter()

    try:
        # Local files are passed directly to pandas.
        source_to_read = source

        # Download remote CSV files before passing their contents to pandas.
        if urlparse(source).scheme in ("http", "https"):
            context = ssl.create_default_context(cafile=certifi.where())
            with urlopen(source, context=context) as response:
                source_to_read = BytesIO(response.read())

        # Read the CSV using PyArrow, its Arrow data types, and skip malformed rows.
        df = pd.read_csv(
            source_to_read,
            engine="pyarrow",
            dtype_backend="pyarrow",
            on_bad_lines="skip",
        )

        # Convert order dates to real datetime values for filtering and analysis.
        if "order_date" in df.columns:
            df["order_date"] = pd.to_datetime(
                df["order_date"], format="mixed", dayfirst=True, errors="coerce"
            )

    # Report CSV syntax or column parsing failures.
    except pd.errors.ParserError as error:
        print(f"CSV parsing error while loading '{source}': {error}")
        return None
    # Report missing files and operating-system read errors.
    except (FileNotFoundError, OSError) as error:
        print(f"File could not be loaded: '{source}' ({error})")
        return None
    # Report any other unexpected loading failure.
    except Exception as error:
        print(f"CSV file '{source}' could not be loaded: {error}")
        return None

    # Calculate elapsed time and report the successful load.
    elapsed = time.perf_counter() - start_time
    print(f"Successfully loaded CSV in {elapsed:.3f} seconds.")

    # Display the number of rows and each dataframe column.
    print(f"Rows: {len(df)}")
    print("Columns:")
    for column in df.columns:
        print(f"  - {column}")

    # Find required dashboard columns that are absent from the dataframe.
    missing_columns = sorted(REQUIRED_COLUMNS - set(df.columns))
    if missing_columns:
        print("WARNING: Missing required dashboard fields:")

        # List every missing field separately.
        for column in missing_columns:
            print(f"  - {column}")

        # Explain the effect of the missing fields.
        print("Some dashboard analytics will not function without these fields.")

    # Return the loaded dataframe to the calling code.
    return df


def create_test_csv():
    # Load the complete sales dataset from Google Drive.
    sales_data = load_csv(DRIVE_CSV_URL)

    # Create a test CSV only when the full file loads successfully.
    if sales_data is not None:
        sales_data.head(10).to_csv("sales_data_test.csv", index=False)
        print("Created sales_data_test.csv with 10 rows.")


def display_initial_rows(data):
    # Stop gracefully if loading failed and no DataFrame is available.
    if data is None:
        print("No data is available to display.")
        return False

    # Explain the valid choices accepted by this function.
    print("\nEnter the number of initial rows to display, 'all', or 'q' to quit.")

    try:
        user_input = input("How many rows would you like to see? ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled. Exiting the program.")
        return False

    # An empty input skips the preview and continues the loop.
    if user_input == "":
        print("Preview skipped. Continuing the program.")
        return True

    # Allow the user to exit the application.
    if user_input in ("q", "quit", "exit"):
        print("Exiting the program.")
        return False

    # The word all displays every row in the DataFrame.
    if user_input == "all":
        print(data.to_string())
        return True

    try:
        row_count = int(user_input)
    except ValueError:
        print("Invalid input. Please enter a positive integer, 'all', or 'q'.")
        return True

    # Reject zero, negative values, and numbers larger than the DataFrame.
    if row_count < 1:
        print("Invalid input. The row count must be at least 1.")
        return True
    if row_count > len(data):
        print(f"Invalid input. This DataFrame contains only {len(data)} rows.")
        return True

    # Display the requested initial rows.
    print(data.head(row_count).to_string(index=False))
    return True


def main():
    # Load the local test data once, then repeatedly ask the user for row counts.
    local_data = load_csv(Path(__file__).with_name("sales_data_test.csv"))

    # Keep the application running until display_initial_rows() requests an exit.
    while True:
        if not display_initial_rows(local_data):
            break


if __name__ == "__main__":
    # Run the application only when this script is executed directly.
    main()
