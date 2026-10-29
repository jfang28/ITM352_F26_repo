import csv
from pathlib import Path

csv_path = Path(__file__).with_name("my_custom_sheet.csv")

with csv_path.open("r", newline="", encoding="utf-8") as csv_file:
    rows = csv.DictReader(csv_file)
    salaries = [int(row["Annual_Salary"]) for row in rows]

average_salary = sum(salaries) / len(salaries)

print(f"Average Annual_Salary: ${average_salary:,.2f}")
print(f"Maximum Annual_Salary: ${max(salaries):,.2f}")
print(f"Minimum Annual_Salary: ${min(salaries):,.2f}")
