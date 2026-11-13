#Inspect the website https://shidler.hawaii.edu/itm/people and note the HTML that displays the people. Using BeautifulSoup, parse the page to extract the HTML.  Use prettify() to print out the HTML (only put the first few lines here). You will need to install beautifulsoup4.

from bs4 import BeautifulSoup
import requests

url = "https://shidler.hawaii.edu/itm/people"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
print(soup.prettify()[:1000])  # Print the first few lines of the HTML
