from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen, Request
import numpy as np
import pandas as pd


def worldometer_coronavirus_scrape():
    '''
    returns general country information for all states in the US on coronavirus

    returns:
    pandas df
    '''
    # reads link
    req = Request('https://www.worldometers.info/coronavirus/country/us/', headers={'User-Agent': 'Mozilla/5.0'})
    page_html = urlopen(req).read()
    page_soup = soup(page_html, "html.parser")

    raw_table = page_soup.find_all("table", {"id": "usa_table_countries_today"})[0]

    rows = raw_table.find_all('tbody')[0].find_all('tr')

    # extra useless rows
    del rows[0]

    cols = []
    for row in rows:
        col = row.find_all('td')
        cols.append(col)
        link_raw = str(row.find_all('a'))
        link_start = link_raw.find('href')
        link_end = link_raw.find('>')




    state_names = []
    total_cases = []
    total_deaths = []
    active_cases = []
    cases_per_mil = []
    deaths_per_mil = []
    total_tests = []
    tests_per_mil = []

    for i in range(len(cols)):
        state_name = cols[i][0].text
        state_names.append(state_name.replace('\n',''))

        total_case = cols[i][1].text
        total_cases.append(total_case)

        total_death = cols[i][3].text
        total_deaths.append(total_death)

        active_case = cols[i][5].text
        active_cases.append(active_case)

        case_per_mil = cols[i][6].text
        cases_per_mil.append(case_per_mil)

        death_per_mil = cols[i][7].text
        deaths_per_mil.append(death_per_mil)

        total_test = cols[i][8].text
        total_tests.append(total_test)

        test_per_mil = cols[i][9].text
        tests_per_mil.append(test_per_mil)

    df = pd.DataFrame({ 
        'state names':state_names,
        'total cases':list_cleaner(total_cases),
        'total deaths':list_cleaner(total_deaths),
        'active cases':list_cleaner(active_cases),
        'cases per mil':list_cleaner(cases_per_mil),
        'deaths per mil':list_cleaner(deaths_per_mil),
        'total tests':list_cleaner(total_tests),
        'tests per mil':list_cleaner(tests_per_mil)
    })

    return df


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

def find_number_cases(df, state):
    return df[0]
    #return df.loc[df['state names'] == 'New York']#['total cases']

df = worldometer_coronavirus_scrape()
print (find_number_cases(df,'New York'))