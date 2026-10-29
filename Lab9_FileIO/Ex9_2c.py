import csv
import os
import stat
from pathlib import Path

# Path to the CSV file, relative to this Python file.
csv_path = Path(__file__).with_name("my_custom_sheet.csv")

# os.path.isfile checks that the path is a file.
# os.access checks whether the current process has read permission.
if os.path.isfile(csv_path) and os.access(csv_path, os.R_OK):
    file_info = csv_path.stat()
    print(f"File: {csv_path.name}")
    print(f"Size: {file_info.st_size} bytes")
    print(f"Permissions: {stat.filemode(file_info.st_mode)}")

    # Open and read the CSV only after confirming that it exists and is readable.
    with csv_path.open("r", newline="", encoding="utf-8") as csv_file:
        rows = csv.DictReader(csv_file)
        salaries = [int(row["Annual_Salary"]) for row in rows]

    average_salary = sum(salaries) / len(salaries)

    print(f"Average Annual_Salary: ${average_salary:,.2f}")
    print(f"Maximum Annual_Salary: ${max(salaries):,.2f}")
    print(f"Minimum Annual_Salary: ${min(salaries):,.2f}")
else:
    print(f"Error: {csv_path} does not exist or is not readable.")
