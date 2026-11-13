# Review the web page at https://data.cityofchicago.org/Historic-Preservation/Landmark-Districts/zidz-sdfj/about_data Inspect the page to view the HTML. Find and note all the <title> tags. Open the URL using  urllib.request.urlopen(url) and print out the response you get. What is this and how do you work with it? You will need to import urllib.request and ssl. Set ssl._create_default_https_context = ssl._create_unverified_context

import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

url = "https://data.cityofchicago.org/Historic-Preservation/Landmark-Districts/zidz-sdfj/about_data"

response = urllib.request.urlopen(url)
print(response.read().decode('utf-8'))