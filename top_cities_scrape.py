from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen as uReq

my_url = "https://en.wikipedia.org/wiki/List_of_largest_cities"

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")

raw_table = page_soup.find_all("table", {"class": "sortable wikitable mw-datatable"})[0]

rows = raw_table.find_all('tbody')[0].find_all('tr')


cols = []

for row in rows:
    col = row.find_all('td')
    cols.append(col)

print (soup.prettify(cols[2][3]))

print ('|')
print ("|")
print ('|')

