import os
import stat
from pathlib import Path

# Path to the CSV file, relative to this Python file.
csv_path = Path(__file__).with_name("my_custom_sheet.csv")

# Check that the path is a file and that it can be read.
if os.path.isfile(csv_path) and os.access(csv_path, os.R_OK):
    file_info = csv_path.stat()
    print(f"File: {csv_path.name}")
    print(f"Size: {file_info.st_size} bytes")
    print(f"Permissions: {stat.filemode(file_info.st_mode)}")

    # Read the file using basic file functions instead of the CSV package.
    with csv_path.open("r", encoding="utf-8") as text_file:
        header = text_file.readline().strip().split(",")
        salary_index = header.index("Annual_Salary")
        salaries = []

        for line in text_file:
            fields = line.strip().split(",")
            salaries.append(int(fields[salary_index]))

    average_salary = sum(salaries) / len(salaries)

    print(f"Average Annual_Salary: ${average_salary:,.2f}")
    print(f"Maximum Annual_Salary: ${max(salaries):,.2f}")
    print(f"Minimum Annual_Salary: ${min(salaries):,.2f}")
else:
    print(f"Error: {csv_path} does not exist or is not readable.")
