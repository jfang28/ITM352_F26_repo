import csv
from pathlib import Path

# Locate the taxi data file relative to this Python file.
taxi_path = Path(__file__).with_name("taxi_1000.csv")

fare_total = 0.0
fare_count = 0
max_trip_miles = 0.0

with taxi_path.open("r", newline="", encoding="utf-8-sig") as taxi_file:
    rows = csv.DictReader(taxi_file)

    for row in rows:
        # Include only records whose fare is greater than $10.
        if row["Fare"]:
            fare = float(row["Fare"])
            if fare > 10:
                fare_total += fare
                fare_count += 1

                # Skip rows where Trip Miles is blank.
                if row["Trip Miles"]:
                    trip_miles = float(row["Trip Miles"])
                    max_trip_miles = max(max_trip_miles, trip_miles)

# Calculate the average fare from the fare values that were read.
fare_average = fare_total / fare_count if fare_count else 0

print(f"Total fares: ${fare_total:,.2f}")
print(f"Average fare: ${fare_average:,.2f}")
print(f"Maximum trip distance: {max_trip_miles:,.1f} miles")