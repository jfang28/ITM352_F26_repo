import requests
from bs4 import BeautifulSoup


url = "https://www.hicentral.com/hawaii-mortgage-rates.php"
response = requests.get(url, timeout=30)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")
rate_table = soup.find("table")

if rate_table is None:
    raise ValueError("Could not find a mortgage rates table on the page.")

current_bank = None
for row in rate_table.find_all("tr")[1:]:
    cells = row.find_all(["td", "th"], recursive=False)
    if not cells:
        continue

    if len(cells) == 5:
        bank_name = cells[0].find(["b", "strong"])
        if bank_name is None:
            raise ValueError("Could not find the lender name in a rate row.")
        current_bank = bank_name.get_text(" ", strip=True)
        rate_cells = cells[1:]
    else:
        rate_cells = cells

    if current_bank is None or len(rate_cells) != 4:
        raise ValueError("Unexpected row format in the mortgage rates table.")

    term, interest_rate, points, apr = (
        cell.get_text(" ", strip=True) or "N/A" for cell in rate_cells
    )
    print(
        f"{current_bank}: {term} | Interest rate: {interest_rate}% "
        f"| Points: {points}% | APR: {apr}%"
    )