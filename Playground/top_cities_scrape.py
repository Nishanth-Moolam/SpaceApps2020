from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen as uReq

#https://www.youtube.com/watch?v=mKxFfjNyj3c

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

city_names = []
city_pops = []


for i in range(len(cols)):
    if i > 1:
        city_name = cols[i][0].text.replace("\n",'')
        city_names.append(city_name)
        city_pop = cols[i][3].text.replace("\n",'')
        city_pops.append(city_pop)

print (city_names[0])
print (city_pops[0])


print ('|')
print ('|')
print ('|')

