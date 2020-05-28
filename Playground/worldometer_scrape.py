from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen, Request
import numpy as np


# base link of worldometer (coronavirus)
worldometer_link_coronavirus = 'https://www.worldometers.info/coronavirus/'

# base link of worldometer (population)
worldometer_link_population = 'https://www.worldometers.info/'


def worldometer_coronavirus_scrape():
    '''
    returns general country information for all countries on coronavirus

    returns:
    - country links - link extensions to the base link that makes url of the country in question
    - country names - name of country
    - total cases - list
    - total_deaths - list
    - total_recovered - list
    - active_cases - list
    - serious_cases - list
    - cases_per_mil - list
    - deaths_per_mil - list
    - total_tests - list 
    - population - list
    - index_names - names for identification and matching from links
    '''
    # reads link
    req = Request('https://www.worldometers.info/coronavirus/', headers={'User-Agent': 'Mozilla/5.0'})
    page_html = urlopen(req).read()
    page_soup = soup(page_html, "html.parser")

    raw_table = page_soup.find_all("table", {"id": "main_table_countries_today"})[0]

    rows = raw_table.find_all('tbody')[0].find_all('tr')
    # extra useless rows
    del rows[0:8]

    country_links = []
    index_names = []

    cols = []
    for row in rows:
        col = row.find_all('td')
        cols.append(col)
        link_raw = str(row.find_all('a'))
        link_start = link_raw.find('href')
        link_end = link_raw.find('>')

        country_links.append(link_raw[link_start+6:link_end-1])
        index_names.append(link_raw[link_start+6:link_end-1].replace('country','').replace('/',''))


    country_names = []
    total_cases = []
    total_deaths = []
    total_recovered = []
    active_cases = []
    serious_cases = []
    cases_per_mil = []
    deaths_per_mil = []
    total_tests = []
    tests_per_mil = []
    population = []

    for i in range(len(cols)):
        country_name = cols[i][1].text
        country_names.append(country_name)

        total_case = cols[i][2].text
        total_cases.append(total_case)

        total_death = cols[i][4].text
        total_deaths.append(total_death)

        total_recover = cols[i][6].text
        total_recovered.append(total_recover)

        active_case = cols[i][7].text
        active_cases.append(active_case)

        serious_case = cols[i][8].text
        serious_cases.append(serious_case)

        case_per_mil = cols[i][9].text
        cases_per_mil.append(case_per_mil)

        death_per_mil = cols[i][10].text
        deaths_per_mil.append(death_per_mil)

        total_test = cols[i][11].text
        total_tests.append(total_test)

        test_per_mil = cols[i][12].text
        tests_per_mil.append(test_per_mil)

        pop = cols[i][13].text
        population.append(pop)

    worldometer_data =  (country_links, country_names, list_cleaner(total_cases), 
                        list_cleaner(total_deaths), list_cleaner(total_recovered), 
                        list_cleaner(active_cases), list_cleaner(serious_cases), 
                        list_cleaner(cases_per_mil), list_cleaner(deaths_per_mil), 
                        list_cleaner(total_tests), list_cleaner(population), 
                         index_names)

    return worldometer_data

def worldometer_population_scrape():
    '''
    returns general country information for all countries

    returns:
    - country_links - link extensions to the base link that makes url of the country in question
    - country_names - name of country
    - population - list
    - yearly_change - list
    - net_change - list
    - density - list
    - land_area - list
    - migrants - list
    - fertility_rate - list
    - median_age - list
    - urban_pop_percent - list
    - world_share - list
    - index_names - names for identification and matching from links

    '''

    req = Request('https://www.worldometers.info/world-population/population-by-country/', headers={'User-Agent': 'Mozilla/5.0'})
    page_html = urlopen(req).read()
    page_soup = soup(page_html, "html.parser")

    raw_table = page_soup.find_all("table", {"id": "example2"})[0]

    rows = raw_table.find_all('tbody')[0].find_all('tr')

    country_links = []
    index_names = []
    cols = []
    for row in rows:
        col = row.find_all('td')
        cols.append(col)
        link_raw = str(row.find_all('a'))
        link_start = link_raw.find('href')
        link_end = link_raw.find('>')

        country_links.append(link_raw[link_start+7:link_end-1])
        index_names.append(link_raw[link_start+7:link_end-1].split('-population/')[1])
    
    country_names = []
    population = []
    yearly_change = []
    net_change = []
    density = []
    land_area = []
    migrants = []
    fertility_rate = []
    median_age = []
    urban_pop_percent = []
    world_share = []

    for i in range(len(cols)):
        country_name = cols[i][1].text
        country_names.append(country_name)

        pop = cols[i][2].text
        population.append(pop)

        yc = cols[i][3].text
        yearly_change.append(yc)

        nc = cols[i][4].text
        net_change.append(nc)

        dense = cols[i][5].text
        density.append(dense)

        la = cols[i][6].text
        land_area.append(la)

        mig = cols[i][7].text
        migrants.append(mig)

        fr = cols[i][8].text
        fertility_rate.append(fr)

        ma = cols[i][9].text
        median_age.append(ma)

        upp = cols[i][10].text
        urban_pop_percent.append(upp)

        ws = cols[i][11].text
        world_share.append(ws)

    worldometer_data =  (country_links, country_names, list_cleaner(population), list_cleaner(yearly_change), 
                        list_cleaner(net_change), list_cleaner(density), list_cleaner(land_area), 
                        list_cleaner(migrants), list_cleaner(fertility_rate), list_cleaner(median_age), 
                        list_cleaner(urban_pop_percent), list_cleaner(world_share), index_names)

    return worldometer_data

def worldometer_graph_data_collector(link, graph_num):
    '''
    helper function to obtain information from graphs in worldometer website
    '''
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    page_html = urlopen(req).read()
    page_soup = soup(page_html, "html.parser")

    try:
        total_data_raw = str(page_soup.find_all("div", {"class": "col-md-12"})[graph_num].find_all('script')[0])

        date_start_init = total_data_raw.find('xAxis')
        date_end_init = total_data_raw.find('yAxis')
        date_data = total_data_raw[date_start_init:date_end_init]
        date_start = date_data.find('[')
        date_end = date_data.find(']')

        # list of dates
        dates_total_data = date_data[date_start+1:date_end].replace('"','').replace("'","").split(',')

        data_start_init = total_data_raw.find('data')
        data_end_init = total_data_raw.find('responsive')
        data = total_data_raw[data_start_init:data_end_init]
        data_start = data.find('[')
        data_end = data.find(']')

        # list of case data
        total_data = list_cleaner(data[data_start+1:data_end].split(','))
    except IndexError:
        dates_total_data = None
        total_data = None

    return (dates_total_data , total_data)

def worldometer_country_scrape(link):
    '''
    given a link to a country info page (specific to coronavirus info pages) returns all relevant information

    returns:
    - country_name - name of country
    - total_cases - tuple of dates, and case data (daily)
    - daily_new_cases - tuple of dates, and new case data (daily)
    - active_cases - tuple of dates, and active data (daily)
    - total_deaths - tuple of dates, and new deaths data (daily)
    - daily_deaths - tuple of dates, and new daily death data (daily)
    '''
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    page_html = urlopen(req).read()
    page_soup = soup(page_html, "html.parser")

    name_raw = page_soup.find_all("div", {"class": "content-inner"})[0].find_all('h1')[0].text

    country_name = str(name_raw)

    total_cases = worldometer_graph_data_collector(link, 0)
    daily_new_cases = worldometer_graph_data_collector(link, 1)
    active_cases = worldometer_graph_data_collector(link, 2)
    total_deaths = worldometer_graph_data_collector(link, 3)
    daily_deaths = worldometer_graph_data_collector(link, 4)


    return (country_name, total_cases, daily_new_cases, active_cases, total_deaths, daily_deaths)

def list_cleaner(list_of_strings):
    '''
    converts a list to a list of floats
    '''
    l = []
    for i in list_of_strings:
        if i == ' ':
            l.append(0.)
        elif i == '':
            l.append(0.)
        elif i == 'null':
            l.append(0.)
        elif i =='N/A':
            l.append(0.)
        elif i =='N.A.':
            l.append(0.)
        else:
            l.append(float(i.replace(',','').replace('%','')))

    return l
