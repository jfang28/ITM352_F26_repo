#Open the URL url = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202603" and note the table of interest rate data. Use .read_html() to extract the interest rate table information as a DataFrame and print out its columns. If you are getting an SSL error you will need to: install the lxml library. set ssl._create_default_https_context = ssl._create_unverified_context
import pandas as pd
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

url = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202603"

tables = pd.read_html(url)
for table in tables:
    print(table.columns)