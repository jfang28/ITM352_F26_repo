# Provide secure HTTPS connections and measure loading time.
import ssl
import time
from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen

# Use pandas to load the sales data.
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
            context = ssl.create_default_context()
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

menu_options = (
    "Display initial rows",
    "Display summary statistics",
    "Show total sales by region",
    "Filter and display sales by region",
    "Search by employee or customer name",
    "Generate custom pivot table",
    "Quit",
)


def get_user_selection(options, prompt):
    print(prompt)
    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")

    choice = input("Enter the number(s) of your choice(s), separated by commas: ").strip()
    if not choice:
        return []

    try:
        indices = [int(item.strip()) - 1 for item in choice.split(",")]
    except ValueError:
        print("Invalid selection. Enter option numbers separated by commas.")
        return []

    if any(index < 0 or index >= len(options) for index in indices):
        print("Invalid selection. Choose numbers from the listed options.")
        return []

    return [options[index] for index in indices]


def generate_custom_pivot_table(data):
    row_options = list(data.columns)
    col_options = row_options
    value_options = list(data.select_dtypes(include=["number"]).columns)
    agg_options = ["sum", "mean", "count"]

    try:
        rows = get_user_selection(row_options, "\nSelect rows (required):")
    except (EOFError, KeyboardInterrupt):
        print("\nCustom pivot table cancelled.")
        return

    if not rows:
        print("Select at least one row field.")
        return
    if len(rows) != len(set(rows)):
        print("Each row field can only be selected once.")
        return
    if any(column not in row_options for column in rows):
        print("Invalid row field selection. Choose from the available row fields.")
        return

    col_options = [col for col in col_options if col not in rows]
    try:
        columns = get_user_selection(
            col_options, "\nSelect columns (optional; press Enter for none):"
        )
    except (EOFError, KeyboardInterrupt):
        print("\nCustom pivot table cancelled.")
        return

    if len(columns) != len(set(columns)):
        print("Each column field can only be selected once.")
        return
    if any(column not in col_options for column in columns):
        print("Invalid column field selection. Choose from the available column fields.")
        return

    available_value_options = [
        option for option in value_options if option not in rows and option not in columns
    ]
    if not available_value_options:
        print("No numeric fields are available to aggregate for these row and column fields.")
        return

    try:
        selected_values = get_user_selection(available_value_options, "\nSelect a value field:")
    except (EOFError, KeyboardInterrupt):
        print("\nCustom pivot table cancelled.")
        return

    if len(selected_values) != 1:
        print("Select exactly one value field.")
        return
    value = selected_values[0]

    try:
        selected_aggregations = get_user_selection(
            agg_options, "\nSelect an aggregation function:"
        )
    except (EOFError, KeyboardInterrupt):
        print("\nCustom pivot table cancelled.")
        return

    if len(selected_aggregations) != 1:
        print("Select exactly one aggregation function.")
        return
    aggregation = selected_aggregations[0]

    pivot_table = pd.pivot_table(
        data,
        index=rows,
        columns=columns or None,
        values=value,
        aggfunc=aggregation,
    )
    print("\nCustom Pivot Table")
    print(pivot_table.to_string())


def display_menu():
    print("\nSales Data Analysis Menu")
    for option_number, option in enumerate(menu_options, start=1):
        print(f"{option_number}. {option}")


def require_columns(data, columns):
    missing_columns = [column for column in columns if column not in data.columns]
    if missing_columns:
        print("This analysis is unavailable. Missing columns: " + ", ".join(missing_columns))
        return False
    return True


def display_summary_statistics(data):
    print("\nSummary Statistics")

    if not require_columns(data, ("quantity", "unit_price", "order_date")):
        return

    numeric_data = data[["quantity", "unit_price"]].apply(pd.to_numeric, errors="coerce")
    print(f"Rows: {len(data)}")
    print(f"Total quantity sold: {numeric_data['quantity'].sum():,.0f}")
    print(f"Average unit price: ${numeric_data['unit_price'].mean():,.2f}")
    print(f"Total sales value: ${(numeric_data['quantity'] * numeric_data['unit_price']).sum():,.2f}")

    valid_dates = data["order_date"].dropna()
    if len(valid_dates) > 0:
        print(f"Date range: {valid_dates.min().date()} to {valid_dates.max().date()}")


def display_sales_by_region(data):
    if not require_columns(data, ("sales_region", "quantity", "unit_price")):
        return

    analysis = data.copy()
    analysis["quantity"] = pd.to_numeric(analysis["quantity"], errors="coerce")
    analysis["unit_price"] = pd.to_numeric(analysis["unit_price"], errors="coerce")
    analysis["sales_value"] = analysis["quantity"] * analysis["unit_price"]
    totals = analysis.groupby("sales_region", dropna=False)["sales_value"].sum()

    print("\nTotal Sales by Region")
    if totals.empty:
        print("No regional sales data is available.")
        return

    for region, total in totals.sort_values(ascending=False).items():
        print(f"{region}: ${total:,.2f}")


def filter_sales_by_region(data):
    if not require_columns(data, ("sales_region",)):
        return

    regions = sorted(str(region) for region in data["sales_region"].dropna().unique())
    if not regions:
        print("No sales regions are available in the data.")
        return

    print("Available regions: " + ", ".join(regions))
    region = input("Enter a sales region: ").strip()
    matches = data[data["sales_region"].astype("string").str.casefold() == region.casefold()]
    print(f"\nFound {len(matches)} matching rows.")
    if len(matches) > 0:
        print(matches.to_string(index=False))


def search_sales(data):
    columns = [column for column in ("employee_name", "customer_name") if column in data.columns]
    if not columns:
        print("This search is unavailable. Employee and customer name columns are missing.")
        return

    search_text = input("Enter a name to search for: ").strip()
    if not search_text:
        print("Search cancelled.")
        return

    matches = pd.Series(False, index=data.index)
    for column in columns:
        matches |= data[column].astype("string").str.contains(search_text, case=False, na=False)

    results = data[matches]
    print(f"\nFound {len(results)} matching rows.")
    if len(results) > 0:
        print(results.to_string(index=False))


def main():
    # Load the local test data once and offer the analysis actions repeatedly.
    local_data = load_csv(Path(__file__).with_name("sales_data_test.csv"))

    if local_data is None:
        print("The sales application cannot continue without valid sales data.")
        return

    while True:
        display_menu()

        try:
            choice = input("Select an option: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting the program.")
            break

        if choice == "1":
            display_initial_rows(local_data)
        elif choice == "2":
            display_summary_statistics(local_data)
        elif choice == "3":
            display_sales_by_region(local_data)
        elif choice == "4":
            filter_sales_by_region(local_data)
        elif choice == "5":
            search_sales(local_data)
        elif choice == "6":
            generate_custom_pivot_table(local_data)
        elif choice in ("7", "q", "quit", "exit"):
            print("Exiting the program.")
            break
        else:
            print(f"Invalid option. Please enter a number from 1 to {len(menu_options)}.")


if __name__ == "__main__":
    # Run the application only when this script is executed directly.
    main()
