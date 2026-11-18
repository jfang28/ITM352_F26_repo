from bs4 import BeautifulSoup
import requests

url = "https://shidler.hawaii.edu/itm/people"
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

people = [
    person.find("h2").get_text(" ", strip=True)
    for person in soup.find_all("article", class_="node-faculty")
    if person.find("h2")
]

print("People found:")
for person in people:
    print(person)
print(f"Number of people found: {len(people)}")