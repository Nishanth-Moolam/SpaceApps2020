import pandas as pd 
import sqlite3
from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen, Request
import numpy as np

import matplotlib.pyplot as plt
import worldometer_scrape as ws 

def gather_data():
    '''
    gathers all worldwide data from scrape, outputs all information
    '''
    (country_links_c, country_names_c, 
    total_cases_c, total_deaths_c, 
    total_recovered_c, active_cases_c, 
    serious_cases_c, cases_per_mil_c, 
    deaths_per_mil_c, total_tests_c, 
    population_c, index_names_c) = ws.worldometer_coronavirus_scrape()

    (country_links_p, country_names_p,
    population_p, yearly_change_p, 
    net_change_p, density_p, 
    land_area_p, migrants_p, 
    fertility_rate_p, median_age_p,
    urban_pop_percent_p, world_share_p,
    index_names_p) = ws.worldometer_population_scrape()

    data = (country_links_c, country_names_c, 
    total_cases_c, total_deaths_c, 
    total_recovered_c, active_cases_c, 
    serious_cases_c, cases_per_mil_c, 
    deaths_per_mil_c, total_tests_c, 
    population_c, index_names_c,
    country_links_p, country_names_p,
    population_p, yearly_change_p, 
    net_change_p, density_p, 
    land_area_p, migrants_p, 
    fertility_rate_p, median_age_p,
    urban_pop_percent_p, world_share_p,
    index_names_p)

    return data

def make_world_df(data):
    '''
    uses worldwide scrape data, organizes into pandas dataframe
    '''
    (country_links_c, country_names_c, 
    total_cases_c, total_deaths_c, 
    total_recovered_c, active_cases_c, 
    serious_cases_c, cases_per_mil_c, 
    deaths_per_mil_c, total_tests_c, 
    population_c, index_names_c,
    country_links_p, country_names_p,
    population_p, yearly_change_p, 
    net_change_p, density_p, 
    land_area_p, migrants_p, 
    fertility_rate_p, median_age_p,
    urban_pop_percent_p, world_share_p,
    index_names_p) = data


    # pandas df data (pop)
    world_data = {
        'name' : index_names_p,
        'population' : population_p,
        'yearly_p_change' : yearly_change_p,
        'net_p_change' : net_change_p,
        'density' : density_p,
        'land_area' : land_area_p,
        'fertility_rate' : fertility_rate_p,
        'median_age' : median_age_p,
        'urban_pop_percent' : urban_pop_percent_p,
        'world_share' : world_share_p
    }

    df_world = pd.DataFrame(world_data, columns = ['name', 'population','yearly_p_change',
                                                    'net_p_change', 'density','land_area',
                                                    'fertility_rate','median_age','urban_pop_percent',
                                                    'world_share','total_c_cases','total_c_deaths',
                                                    'total_c_recovered','active_c_cases','serious_c_cases',
                                                    'c_cases_per_mil','c_deaths_per_mil','total_c_tests'])

    # sorts and places corona data into pop data
    for i in range(len(index_names_c)):
        df_world.loc[df_world['name'] == index_names_c[i], ['total_c_cases']] = total_cases_c[i]
        df_world.loc[df_world['name'] == index_names_c[i], ['total_c_deaths']] = total_deaths_c[i]
        df_world.loc[df_world['name'] == index_names_c[i], ['total_c_recovered']] = total_recovered_c[i]
        df_world.loc[df_world['name'] == index_names_c[i], ['active_c_cases']] = active_cases_c[i]
        df_world.loc[df_world['name'] == index_names_c[i], ['serious_c_cases']] = serious_cases_c[i]
        df_world.loc[df_world['name'] == index_names_c[i], ['c_cases_per_mil']] = cases_per_mil_c[i]
        df_world.loc[df_world['name'] == index_names_c[i], ['c_deaths_per_mil']] = deaths_per_mil_c[i]
        df_world.loc[df_world['name'] == index_names_c[i], ['total_c_tests']] = total_tests_c[i]

    return df_world
    
print (make_world_df(gather_data()).head())

#---------------------------------------------------------------------------------------------------

'''
now I need to put this data into a database. 

its prob easier to make a pandas df, then make that into a db table

1 table for world info (all countries) - done
1 table per country named after index name
'''

# remember to comment out
country_links_c = ['country/brazil/']


#takes around 10 min with full list
'''
countries_data = []
for link in country_links_c:
    data = ws.worldometer_country_scrape(ws.worldometer_link_coronavirus+link)
    countries_data.append(data)
'''


def create_world_table():
    sql = '''
    CREATE TABLE IF NOT EXISTS world(
        name TEXT,
        population REAL,
        yearly_p_change REAL,
        net_p_change REAL, 
        density REAL,
        land_area REAL, 
        fertility_rate REAL,
        median_age REAL, 
        urban_pop_percent REAL, 
        world_share REAL, 
        total_c_cases REAL,
        total_c_deaths REAL, 
        total_c_recovered REAL,
        active_c_cases REAL,
        serious_c_cases REAL,
        c_cases_per_mil REAL,
        c_deaths_per_mil REAL,
        total_c_tests REAL,
    )
    '''
    c.execute(sql)

