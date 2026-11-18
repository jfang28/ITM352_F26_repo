from bs4 import BeautifulSoup
import requests


url = "https://shidler.hawaii.edu/itm/people"
response = requests.get(url, timeout=30)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

people = []
for card in soup.find_all("article", class_="node-faculty"):
    name = card.select_one("h2")
    email = card.select_one(".field-email .field-item")
    if name is None or email is None:
        raise ValueError("A faculty card is missing a name or email.")
    people.append(
        (name.get_text(" ", strip=True), email.get_text(" ", strip=True))
    )

for name, email in people:
    print(f"{name}: {email}")
