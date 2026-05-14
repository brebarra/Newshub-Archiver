import requests
from bs4 import BeautifulSoup as Soup
import os
import csv

ATTRS = ["loc"]

def parse_sitemap(url):
    if not url:
        return False
    
    response = requests.get(url)
    
    if response.status_code != 200:
        return False
    
    soup = Soup(response.content, "xml")
    
    for sitemap in soup.find_all("sitemap"):
        loc = sitemap.find("loc").text
        parse_sitemap(loc)
        
    root = os.path.dirname(os.path.abspath(__file__))
    
    urls = soup.find_all("url")
    
    rows = []
    for url in urls:
        row = []
        for attr in ATTRS:
            found_attr = url.find(attr)
            # Use "n/a" if the attribute is not found, otherwise get its text.
            row.append(found_attr.text if found_attr else "n/a")
        rows.append(row)

    # Append the data to the CSV file.
    with open(os.path.join(root, "data.csv"), "a+", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)
        print("Data written")
        
parse_sitemap('https://www.newshub.co.nz/home.sitemapindex.xml')
