"""Interactive command-line sales dashboard using Pandas pivot tables."""

from datetime import datetime
from time import perf_counter

import pandas as pd


SALES_DATA_URL = (
    "https://drive.google.com/uc?export=download"
    "&id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA"
)

# These fields are needed across the dashboard's predefined analyses.
REQUIRED_COLUMNS = (
    "sales_region",
    "employee_id",
    "product_category",
    "product_number",
    "produce_name",
    "customer_type",
    "customer_state",
    "order_type",
    "quantity",
    "unit_price",
)


def load_sales_data():
    """Download the Google Drive CSV and report its load status and schema."""
    print("Loading sales_data.csv from Google Drive...")
    start_time = perf_counter()

    try:
        # Let Pandas download and parse the CSV directly from its Google Drive URL.
        data = pd.read_csv(SALES_DATA_URL)
    except (
        TimeoutError,
        OSError,
        UnicodeDecodeError,
        pd.errors.EmptyDataError,
        pd.errors.ParserError,
        ValueError,
    ) as error:
        print(
            "ERROR: Unable to load sales_data.csv "
            f"({type(error).__name__}): {error}"
        )
        return None

    # Fill blank cells before the data is passed to dashboard analyses.
    data = data.fillna(0)
    elapsed = perf_counter() - start_time
    loaded_at = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

    print(f"sales_data.csv loaded successfully at {loaded_at}.")
    print(f"Load time: {elapsed:.3f} seconds")
    print(f"Rows of data: {len(data):,}")
    print("Available columns:")
    for column in data.columns:
        print(f"  - {column}")

    # Warn about absent fields while allowing available dashboard analyses to continue.
    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in data.columns
    ]
    if missing_columns:
        print("\nWARNING: The following required analytics fields are missing:")
        for column in missing_columns:
            print(f"  - {column}")
        print("Some dashboard analytics may not work without these fields.")

    return data


def require_columns(data, columns):
    """Return whether all columns required for an analysis are available."""
    missing_columns = [column for column in columns if column not in data.columns]
    if missing_columns:
        print("This analysis is unavailable. Missing columns: " + ", ".join(missing_columns))
        return False
    return True


def make_analysis_data(data, required_columns):
    """Copy required fields and calculate numeric quantities, prices, and sales."""
    if not require_columns(data, required_columns):
        return None

    analysis = data.copy()
    for column in ("quantity", "unit_price"):
        if column in analysis.columns:
            analysis[column] = pd.to_numeric(
                analysis[column], errors="coerce"
            ).fillna(0)
    if "quantity" in analysis.columns and "unit_price" in analysis.columns:
        # Sales value is the line-item revenue: quantity multiplied by unit price.
        analysis["sales_value"] = analysis["quantity"] * analysis["unit_price"]
    return analysis


def print_pivot(title, pivot):
    """Print a descriptive title and a pivot table in the terminal."""
    print(f"\n{title}")
    if pivot.empty:
        print("No data is available for this analysis.")
    else:
        print(pivot.to_string())


# Menu item 1: display a validated number of rows, all rows, or skip the preview.
def show_first_rows(data):
    """Display the first n rows, where n is chosen by the user."""
    available_rows = len(data)
    if available_rows == 0:
        print("No data rows are available to display.")
        return

    while True:
        print(f"\nRows available: {available_rows}")
        print(f"Enter a number 1 to {available_rows}")
        print("To see all rows, enter 'all'")
        print("To skip preview, press Enter")
        try:
            selection = input("Your choice: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nRow display cancelled.")
            return

        # An empty response explicitly skips the preview without printing rows.
        if not selection:
            print("Preview skipped.")
            return
        if selection == "all":
            print(data.to_string(index=False))
            return

        try:
            row_count = int(selection)
        except ValueError:
            print("Invalid input. Enter a whole number in the available range or 'all'.")
            continue
        if row_count < 1 or row_count > available_rows:
            print(f"Invalid input. Enter a number from 1 to {available_rows}.")
            continue

        print(data.head(row_count).to_string(index=False))
        return


# Menu item 2: sum quantity-times-price sales by region and order type.
def total_sales_by_region_and_type(data):
    """Display total line-item sales, grouped by region and order type."""
    analysis = make_analysis_data(
        data, ("sales_region", "order_type", "quantity", "unit_price")
    )
    if analysis is None:
        return

    pivot = pd.pivot_table(
        analysis,
        values="sales_value",
        index="sales_region",
        columns="order_type",
        aggfunc="sum",
        fill_value=0,
        margins=True,
        margins_name="Total",
    )
    print_pivot("Total Sales by Region and Order Type", pivot)


# Menu item 3: average quantity-times-price sales by region, state, and order type.
def average_sales_by_region_state_and_type(data):
    """Display average line-item sales by region, state, and order type."""
    analysis = make_analysis_data(
        data,
        ("sales_region", "customer_state", "order_type", "quantity", "unit_price"),
    )
    if analysis is None:
        return

    pivot = pd.pivot_table(
        analysis,
        values="sales_value",
        index=["sales_region", "customer_state"],
        columns="order_type",
        aggfunc="mean",
        fill_value=0,
    )
    print_pivot("Average Sales by Region, State, and Order Type", pivot)


# Menu item 4: sum sales for each state, customer type, and order type.
def sales_by_customer_type_and_order_type_by_state(data):
    """Display total sales by customer type and order type for each state."""
    analysis = make_analysis_data(
        data,
        ("customer_type", "customer_state", "order_type", "quantity", "unit_price"),
    )
    if analysis is None:
        return

    pivot = pd.pivot_table(
        analysis,
        values="sales_value",
        index=["customer_state", "customer_type", "order_type"],
        aggfunc="sum",
        fill_value=0,
    )
    print_pivot("Sales by State, Customer Type, and Order Type", pivot)


# Menu item 5: sum quantities and unit prices for products within each region.
def total_quantity_and_price_by_region_and_product(data):
    """Display total quantity and unit-price sums by region and product."""
    analysis = make_analysis_data(
        data,
        (
            "sales_region",
            "product_category",
            "product_number",
            "produce_name",
            "quantity",
            "unit_price",
        ),
    )
    if analysis is None:
        return

    pivot = pd.pivot_table(
        analysis,
        values=["quantity", "unit_price"],
        index=["sales_region", "product_category", "product_number", "produce_name"],
        aggfunc="sum",
        fill_value=0,
    )
    print_pivot("Total Quantity and Unit-Price Sum by Region and Product", pivot)


# Menu item 6: sum quantities and unit prices for each order/customer type pair.
def total_quantity_and_price_by_customer_type(data):
    """Display total quantity and unit-price sums by order and customer type."""
    analysis = make_analysis_data(
        data, ("order_type", "customer_type", "quantity", "unit_price")
    )
    if analysis is None:
        return

    pivot = pd.pivot_table(
        analysis,
        values=["quantity", "unit_price"],
        index=["order_type", "customer_type"],
        aggfunc="sum",
        fill_value=0,
    )
    print_pivot("Total Quantity and Unit-Price Sum by Order and Customer Type", pivot)


# Menu item 7: find minimum and maximum unit prices within each product category.
def max_and_min_price_by_category(data):
    """Display minimum and maximum unit prices for each product category."""
    analysis = make_analysis_data(data, ("product_category", "unit_price"))
    if analysis is None:
        return

    pivot = pd.pivot_table(
        analysis,
        values="unit_price",
        index="product_category",
        aggfunc=["min", "max"],
        fill_value=0,
    )
    print_pivot("Minimum and Maximum Sales Price by Category", pivot)


# Menu item 8: count distinct employee IDs in each sales region.
def unique_employees_by_region(data):
    """Display the number of unique employee IDs in each sales region."""
    if not require_columns(data, ("sales_region", "employee_id")):
        return

    # R1 replaces blanks with zero; exclude those placeholders from employee counts.
    employee_data = data[["sales_region", "employee_id"]].copy()
    employee_data["employee_id"] = (
        employee_data["employee_id"].astype("string").replace("0", pd.NA)
    )
    pivot = pd.pivot_table(
        employee_data,
        values="employee_id",
        index="sales_region",
        aggfunc=pd.Series.nunique,
        fill_value=0,
    ).rename(columns={"employee_id": "unique_employee_count"})
    print_pivot("Number of Unique Employees by Region", pivot)


def get_user_selection(options, prompt, allow_empty=False):
    """Return one or more validated options; return None if input is cancelled."""
    while True:
        print(prompt)
        for number, option in enumerate(options, start=1):
            print(f"{number}. {option}")

        try:
            choice = input("Enter selection number(s), separated by commas: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSelection cancelled.")
            return None

        if not choice and allow_empty:
            return []
        if not choice:
            print("Make at least one selection.")
            continue

        try:
            indices = [int(item.strip()) - 1 for item in choice.split(",")]
        except ValueError:
            print("Enter valid option numbers separated by commas.")
            continue
        if len(indices) != len(set(indices)):
            print("Each option can only be selected once.")
            continue
        if any(index < 0 or index >= len(options) for index in indices):
            print("Choose numbers from the listed options.")
            continue
        return [options[index] for index in indices]


# Menu item 9: prompt for fields and aggregation, then display a custom pivot.
def create_custom_pivot_table(data):
    """Prompt for multiple pivot dimensions, values, and aggregations."""
    row_fields = list(data.columns)
    selected_rows = get_user_selection(row_fields, "\nSelect rows:")
    if not selected_rows:
        return

    available_columns = [
        field for field in data.columns if field not in selected_rows
    ]
    selected_columns = get_user_selection(
        available_columns,
        "\nSelect columns (optional; press Enter for no grouping):",
        allow_empty=True,
    )
    if selected_columns is None:
        return

    value_fields = [
        field
        for field in data.select_dtypes(include="number").columns
        if field not in selected_rows and field not in selected_columns
    ]
    if not value_fields:
        print("No numeric fields are available to aggregate for these selections.")
        return

    selected_values = get_user_selection(value_fields, "\nSelect values:")
    if not selected_values:
        return

    aggregations = ("sum", "mean", "count", "min", "max")
    selected_aggregations = get_user_selection(
        aggregations, "\nSelect aggregation function(s):"
    )
    if not selected_aggregations:
        return

    try:
        # Pandas produces one set of results for each selected aggregation/value pair.
        pivot = pd.pivot_table(
            data,
            index=selected_rows,
            columns=selected_columns or None,
            values=selected_values[0] if len(selected_values) == 1 else selected_values,
            aggfunc=(
                selected_aggregations[0]
                if len(selected_aggregations) == 1
                else selected_aggregations
            ),
            fill_value=0,
        )
    except (KeyError, TypeError, ValueError) as error:
        print(f"Could not create the pivot table ({type(error).__name__}): {error}")
        return
    print_pivot("Custom Pivot Table", pivot)


# Menu item 10: stop the dashboard loop.
def exit_dashboard(data):
    """Print the exit message and signal the menu loop to stop."""
    print("Exiting the Sales Data Dashboard.")
    return False


# Keep menu configuration in one ordered tuple so options can be reordered or extended.
MENU_ITEMS = (
    ("Show the first n rows of sales data", show_first_rows),
    ("Total sales by region and order_type", total_sales_by_region_and_type),
    (
        "Average sales by region with average sales by state and sale type",
        average_sales_by_region_state_and_type,
    ),
    (
        "Sales by customer type and order type by state",
        sales_by_customer_type_and_order_type_by_state,
    ),
    (
        "Total sales quantity and price by region and product",
        total_quantity_and_price_by_region_and_product,
    ),
    (
        "Total sales quantity and price by customer type",
        total_quantity_and_price_by_customer_type,
    ),
    ("Max and min sales price of sales by category", max_and_min_price_by_category),
    ("Number of unique employees by region", unique_employees_by_region),
    ("Create a custom pivot table", create_custom_pivot_table),
    ("Exit", exit_dashboard),
)


def display_menu():
    """Print the dashboard title and numbered menu options."""
    print("\n--- Sales Data Dashboard ---")
    for number, (label, _) in enumerate(MENU_ITEMS, start=1):
        print(f"{number}. {label}")


def main():
    """Load sales data and dispatch menu selections to their handlers."""
    sales_data = load_sales_data()
    if sales_data is None:
        raise SystemExit(1)

    while True:
        display_menu()
        try:
            selection = input("Select an option: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting the Sales Data Dashboard.")
            return

        try:
            menu_number = int(selection)
        except ValueError:
            print(f"Enter a number from 1 to {len(MENU_ITEMS)}.")
            continue
        if menu_number < 1 or menu_number > len(MENU_ITEMS):
            print(f"Enter a number from 1 to {len(MENU_ITEMS)}.")
            continue

        # Each menu tuple binds its displayed label to the function that performs it.
        handler = MENU_ITEMS[menu_number - 1][1]
        if handler(sales_data) is False:
            return


if __name__ == "__main__":
    main()
