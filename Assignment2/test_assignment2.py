"""Focused tests for dashboard pivots and menu configuration."""

import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import Mock, patch


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


class DashboardDataHelperTests(unittest.TestCase):
    """Cover shared loading, validation, preparation, and output helpers."""

    def test_require_columns_reports_missing_fields(self):
        data = sample_sales_data()
        output = StringIO()
        with redirect_stdout(output):
            self.assertTrue(dashboard.require_columns(data, ("sales_region",)))
            self.assertFalse(dashboard.require_columns(data, ("missing_field",)))
        self.assertIn("Missing columns: missing_field", output.getvalue())

    def test_make_analysis_data_coerces_values_without_mutating_source(self):
        data = sample_sales_data()
        data["quantity"] = ["2", "invalid", "1"]
        data["unit_price"] = ["10", "5", "invalid"]

        analysis = dashboard.make_analysis_data(
            data, ("quantity", "unit_price")
        )

        self.assertEqual(analysis["sales_value"].tolist(), [20, 0, 0])
        self.assertEqual(data["quantity"].tolist(), ["2", "invalid", "1"])

    def test_print_pivot_formats_results(self):
        pivot = dashboard.pd.DataFrame({"quantity": [5]}, index=["West"])
        output = StringIO()
        with redirect_stdout(output):
            dashboard.print_pivot("Quantity by Region", pivot)
        self.assertIn("Quantity by Region", output.getvalue())
        self.assertIn("West", output.getvalue())
        self.assertIn("5", output.getvalue())

    def test_print_pivot_reports_empty_results(self):
        output = StringIO()
        with redirect_stdout(output):
            dashboard.print_pivot("Empty Analysis", dashboard.pd.DataFrame())
        self.assertIn("No data is available", output.getvalue())


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


class DashboardInputHelperTests(unittest.TestCase):
    """Cover reusable validated selection input used by custom pivots."""

    def test_get_user_selection_accepts_multiple_options(self):
        options = ("region", "employee", "order type")
        with patch("builtins.input", return_value="1,3"):
            selected = dashboard.get_user_selection(options, "Select fields:")
        self.assertEqual(selected, ["region", "order type"])

    def test_get_user_selection_retries_duplicates_and_out_of_range(self):
        options = ("region", "employee", "order type")
        output = StringIO()
        with patch("builtins.input", side_effect=["1,1", "0", "2,3"]):
            with redirect_stdout(output):
                selected = dashboard.get_user_selection(options, "Select fields:")
        self.assertEqual(selected, ["employee", "order type"])
        self.assertIn("Each option can only be selected once", output.getvalue())
        self.assertIn("Choose numbers from the listed options", output.getvalue())

    def test_get_user_selection_returns_none_when_cancelled(self):
        output = StringIO()
        with patch("builtins.input", side_effect=EOFError):
            with redirect_stdout(output):
                selected = dashboard.get_user_selection(("region",), "Select fields:")
        self.assertIsNone(selected)
        self.assertIn("Selection cancelled", output.getvalue())


class DashboardMenuTests(unittest.TestCase):
    """Ensure every ordered menu item is connected to an action function."""

    def test_menu_contains_requested_actions_in_order(self):
        labels = [label for label, _ in dashboard.MENU_ITEMS]
        self.assertEqual(len(labels), 10)
        self.assertEqual(labels[0], "Show the first n rows of sales data")
        self.assertEqual(labels[-1], "Exit")
        self.assertTrue(all(callable(handler) for _, handler in dashboard.MENU_ITEMS))

    def test_display_menu_shows_numbered_actions(self):
        output = StringIO()
        with redirect_stdout(output):
            dashboard.display_menu()
        self.assertIn("1. Show the first n rows of sales data", output.getvalue())
        self.assertIn("10. Exit", output.getvalue())

    def test_exit_dashboard_signals_the_menu_loop_to_stop(self):
        output = StringIO()
        with redirect_stdout(output):
            result = dashboard.exit_dashboard(sample_sales_data())
        self.assertIs(result, False)
        self.assertIn("Exiting the Sales Data Dashboard.", output.getvalue())

    def test_main_exits_if_data_cannot_be_loaded(self):
        with patch.object(dashboard, "load_sales_data", return_value=None):
            with self.assertRaises(SystemExit) as error:
                dashboard.main()
        self.assertEqual(error.exception.code, 1)

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


class DashboardRowSelectionTests(unittest.TestCase):
    """Verify per-analysis row ranges and lists select only requested records."""

    def select_rows(self, selections):
        with patch("builtins.input", side_effect=selections):
            return dashboard.select_analysis_rows(sample_sales_data())

    def test_selects_inclusive_row_range(self):
        selected = self.select_rows(["1-2"])
        self.assertEqual(selected["quantity"].tolist(), [2, 3])

    def test_selects_list_in_requested_order(self):
        selected = self.select_rows(["3,1"])
        self.assertEqual(selected["produce_name"].tolist(), ["Gift Basket", "Olive Oil"])

    def test_retries_out_of_range_selection(self):
        output = StringIO()
        with patch("builtins.input", side_effect=["1-4", "2"]):
            with redirect_stdout(output):
                selected = dashboard.select_analysis_rows(sample_sales_data())
        self.assertEqual(selected["quantity"].tolist(), [3])
        self.assertIn("Choose row numbers from 1 to 3", output.getvalue())

    def test_rejects_duplicate_rows(self):
        output = StringIO()
        with patch("builtins.input", side_effect=["1-2,2", "1,3"]):
            with redirect_stdout(output):
                selected = dashboard.select_analysis_rows(sample_sales_data())
        self.assertEqual(selected["quantity"].tolist(), [2, 1])
        self.assertIn("Each row can only be selected once", output.getvalue())

    def test_can_cancel_analysis_row_selection(self):
        with patch("builtins.input", return_value="q"):
            selected = dashboard.select_analysis_rows(sample_sales_data())
        self.assertIsNone(selected)

    def test_blank_selection_uses_all_rows(self):
        data = sample_sales_data()
        with patch("builtins.input", return_value=""):
            selected = dashboard.select_analysis_rows(data)
        self.assertIs(selected, data)

    def test_empty_data_does_not_prompt_for_rows(self):
        data = sample_sales_data().iloc[0:0]
        with patch("builtins.input") as user_input:
            selected = dashboard.select_analysis_rows(data)
        self.assertTrue(selected.empty)
        user_input.assert_not_called()

    def test_dashboard_passes_only_selected_rows_to_analysis(self):
        data = sample_sales_data()
        analysis = Mock()
        menu_items = (("Test analysis", analysis), ("Exit", dashboard.exit_dashboard))
        with (
            patch.object(dashboard, "load_sales_data", return_value=data),
            patch.object(dashboard, "MENU_ITEMS", menu_items),
            patch.object(dashboard, "display_menu"),
            patch("builtins.input", side_effect=["1", "1-2", "2"]),
            redirect_stdout(StringIO()),
        ):
            dashboard.main()
        self.assertEqual(analysis.call_args.args[0]["quantity"].tolist(), [2, 3])


class DashboardDatasetTests(unittest.TestCase):
    """Verify dataset selection and loading behavior."""

    def test_selects_alternate_dataset(self):
        output = StringIO()
        with patch("builtins.input", return_value="2"):
            with redirect_stdout(output):
                source = dashboard.select_sales_data_source()
        self.assertEqual(source, dashboard.SALES_DATA_SOURCES[1])
        self.assertIn("Alternate sample sales data", output.getvalue())

    def test_retries_invalid_dataset_selection(self):
        output = StringIO()
        with patch("builtins.input", side_effect=["3", "1"]):
            with redirect_stdout(output):
                source = dashboard.select_sales_data_source()
        self.assertEqual(source, dashboard.SALES_DATA_SOURCES[0])
        self.assertIn("Enter a number from 1 to 2", output.getvalue())

    def test_can_cancel_dataset_selection(self):
        output = StringIO()
        with patch("builtins.input", return_value="q"):
            with redirect_stdout(output):
                source = dashboard.select_sales_data_source()
        self.assertIsNone(source)
        self.assertIn("selection cancelled", output.getvalue().lower())

    def test_loads_alternate_dataset(self):
        output = StringIO()
        with patch("builtins.input", return_value="2"):
            with redirect_stdout(output):
                data = dashboard.load_sales_data()
        self.assertEqual(len(data), 6)
        self.assertTrue(set(dashboard.REQUIRED_COLUMNS).issubset(data.columns))
        self.assertIn("Island Gift Basket", data["produce_name"].values)

    def test_loads_original_source_and_fills_blank_cells(self):
        data = sample_sales_data()
        data["customer_state"] = data["customer_state"].astype(object)
        data.loc[1, "customer_state"] = None
        output = StringIO()
        with patch("builtins.input", return_value="1"):
            with patch.object(dashboard.pd, "read_csv", return_value=data) as read_csv:
                with redirect_stdout(output):
                    loaded_data = dashboard.load_sales_data()
        read_csv.assert_called_once_with(dashboard.SALES_DATA_URL)
        self.assertEqual(loaded_data.loc[1, "customer_state"], 0)
        self.assertIn("Original sales data", output.getvalue())

    def test_load_failure_is_reported_without_raising(self):
        output = StringIO()
        with patch("builtins.input", return_value="2"):
            with patch.object(
                dashboard.pd,
                "read_csv",
                side_effect=dashboard.pd.errors.ParserError("invalid CSV"),
            ):
                with redirect_stdout(output):
                    data = dashboard.load_sales_data()
        self.assertIsNone(data)
        self.assertIn("Unable to load", output.getvalue())
        self.assertIn("ParserError", output.getvalue())

    def test_cancelled_dataset_selection_does_not_read_file(self):
        with patch("builtins.input", return_value="q"):
            with patch.object(dashboard.pd, "read_csv") as read_csv:
                data = dashboard.load_sales_data()
        self.assertIsNone(data)
        read_csv.assert_not_called()

if __name__ == "__main__":
    unittest.main()
