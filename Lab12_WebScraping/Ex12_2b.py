import pandas as pd
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

url = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202603"

tables = pd.read_html(url)
for table in tables:
    for _, row in table.iterrows():
        print(row["1 Mo"])