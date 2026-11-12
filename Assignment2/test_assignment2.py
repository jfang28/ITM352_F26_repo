"""Focused tests for dashboard pivots and menu configuration."""

import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).parent))
import Assignment2 as dashboard


def sample_sales_data():
    """Return small data with known totals for each dashboard analysis."""
    return dashboard.pd.DataFrame(
        {
            "sales_region": ["West", "West", "East"],
            "employee_id": ["E1", "E2", "E1"],
            "product_category": ["Oil", "Oil", "Gift"],
            "product_number": ["P1", "P1", "P2"],
            "produce_name": ["Olive Oil", "Olive Oil", "Gift Basket"],
            "customer_type": ["Individual", "Business", "Individual"],
            "customer_state": ["HI", "HI", "CA"],
            "order_type": ["Retail", "Wholesale", "Retail"],
            "quantity": [2, 3, 1],
            "unit_price": [10, 4, 20],
        }
    )


class DashboardPivotTests(unittest.TestCase):
    """Check that the predefined analyses aggregate the intended data."""

    def get_pivot(self, handler, data=None):
        data = data if data is not None else sample_sales_data()
        with patch.object(dashboard, "print_pivot") as output:
            handler(data)
        return output.call_args.args[1] if output.called else None

    def test_total_sales_by_region_and_type(self):
        pivot = self.get_pivot(dashboard.total_sales_by_region_and_type)
        self.assertEqual(pivot.loc["West", "Retail"], 20)
        self.assertEqual(pivot.loc["West", "Wholesale"], 12)
        self.assertEqual(pivot.loc["East", "Retail"], 20)
        self.assertEqual(pivot.loc["Total", "Total"], 52)

    def test_average_sales_by_region_state_and_type(self):
        pivot = self.get_pivot(dashboard.average_sales_by_region_state_and_type)
        self.assertEqual(pivot.loc[("West", "HI"), "Retail"], 20)
        self.assertEqual(pivot.loc[("West", "HI"), "Wholesale"], 12)
        self.assertEqual(pivot.loc[("East", "CA"), "Retail"], 20)

    def test_sales_by_customer_type_state_and_order_type(self):
        pivot = self.get_pivot(
            dashboard.sales_by_customer_type_and_order_type_by_state
        )
        self.assertEqual(pivot.at[("HI", "Individual", "Retail"), "sales_value"], 20)
        self.assertEqual(pivot.at[("HI", "Business", "Wholesale"), "sales_value"], 12)

    def test_quantity_and_price_by_region_and_product(self):
        pivot = self.get_pivot(
            dashboard.total_quantity_and_price_by_region_and_product
        )
        self.assertEqual(pivot.loc[("West", "Oil", "P1", "Olive Oil"), "quantity"], 5)
        self.assertEqual(pivot.loc[("West", "Oil", "P1", "Olive Oil"), "unit_price"], 14)

    def test_quantity_and_price_by_customer_type(self):
        pivot = self.get_pivot(dashboard.total_quantity_and_price_by_customer_type)
        self.assertEqual(pivot.loc[("Retail", "Individual"), "quantity"], 3)
        self.assertEqual(pivot.loc[("Retail", "Individual"), "unit_price"], 30)
        self.assertEqual(pivot.loc[("Wholesale", "Business"), "quantity"], 3)

    def test_minimum_and_maximum_price_by_category(self):
        pivot = self.get_pivot(dashboard.max_and_min_price_by_category)
        self.assertEqual(pivot.loc["Oil", ("min", "unit_price")], 4)
        self.assertEqual(pivot.loc["Oil", ("max", "unit_price")], 10)

    def test_unique_employee_count_by_region(self):
        pivot = self.get_pivot(dashboard.unique_employees_by_region)
        self.assertEqual(pivot.loc["West", "unique_employee_count"], 2)
        self.assertEqual(pivot.loc["East", "unique_employee_count"], 1)

    def test_zero_placeholder_is_not_counted_as_an_employee(self):
        data = sample_sales_data()
        data["employee_id"] = ["0", "E2", "E1"]
        pivot = self.get_pivot(dashboard.unique_employees_by_region, data)
        self.assertEqual(pivot.loc["West", "unique_employee_count"], 1)

    def test_missing_field_warns_without_raising(self):
        data = sample_sales_data().drop(columns=["order_type"])
        output = StringIO()
        with redirect_stdout(output):
            pivot = self.get_pivot(
                dashboard.total_sales_by_region_and_type, data=data
            )
        self.assertIsNone(pivot)
        self.assertIn("Missing columns: order_type", output.getvalue())

    def test_custom_pivot_uses_validated_selections(self):
        data = sample_sales_data()
        with patch("builtins.input", side_effect=["1", "", "1", "1"]):
            with patch.object(dashboard, "print_pivot") as output:
                dashboard.create_custom_pivot_table(data)
        pivot = output.call_args.args[1]
        self.assertEqual(pivot.loc["West", "quantity"], 5)
        self.assertEqual(pivot.loc["East", "quantity"], 1)

    def test_custom_pivot_supports_multiple_values_and_aggregations(self):
        data = sample_sales_data()
        # Select region and employee rows, order type columns, both numeric
        # values, and both sum and mean aggregations.
        with patch("builtins.input", side_effect=["1,2", "6", "1,2", "1,2"]):
            with patch.object(dashboard, "print_pivot") as output:
                dashboard.create_custom_pivot_table(data)

        pivot = output.call_args.args[1]
        self.assertEqual(pivot.loc[("West", "E1"), ("sum", "quantity", "Retail")], 2)
        self.assertEqual(pivot.loc[("West", "E1"), ("mean", "unit_price", "Retail")], 10)
        self.assertEqual(
            list(pivot.index.names), ["sales_region", "employee_id"]
        )

    def test_custom_pivot_retries_invalid_choice(self):
        data = sample_sales_data()
        with patch("builtins.input", side_effect=["0", "1", "", "1", "1"]):
            with patch.object(dashboard, "print_pivot") as output:
                dashboard.create_custom_pivot_table(data)
        self.assertTrue(output.called)
        self.assertEqual(output.call_args.args[1].loc["West", "quantity"], 5)


class DashboardMenuTests(unittest.TestCase):
    """Ensure every ordered menu item is connected to an action function."""

    def test_menu_contains_requested_actions_in_order(self):
        labels = [label for label, _ in dashboard.MENU_ITEMS]
        self.assertEqual(len(labels), 10)
        self.assertEqual(labels[0], "Show the first n rows of sales data")
        self.assertEqual(labels[-1], "Exit")
        self.assertTrue(all(callable(handler) for _, handler in dashboard.MENU_ITEMS))

    def test_first_rows_blank_input_skips_preview(self):
        output = StringIO()
        with patch("builtins.input", return_value=""):
            with redirect_stdout(output):
                dashboard.show_first_rows(sample_sales_data())
        self.assertIn("Preview skipped.", output.getvalue())
        self.assertNotIn("Olive Oil", output.getvalue())

    def test_first_rows_all_displays_every_row(self):
        output = StringIO()
        with patch("builtins.input", return_value="all"):
            with redirect_stdout(output):
                dashboard.show_first_rows(sample_sales_data())
        self.assertIn("Olive Oil", output.getvalue())
        self.assertIn("Gift Basket", output.getvalue())

    def test_first_rows_retries_invalid_values(self):
        output = StringIO()
        with patch("builtins.input", side_effect=["not a number", "4", "2"]):
            with redirect_stdout(output):
                dashboard.show_first_rows(sample_sales_data())
        self.assertIn("Invalid input.", output.getvalue())
        self.assertIn("Rows available: 3", output.getvalue())
        self.assertEqual(output.getvalue().count("Olive Oil"), 2)


if __name__ == "__main__":
    unittest.main()
