import pandas as pd 
import numpy as np
from sqlalchemy import create_engine

import matplotlib.pyplot as plt
import worldometer_scrape as ws 

engine = create_engine('sqlite://', echo=False)

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

    df_world = pd.DataFrame(world_data, columns = ['name', 'links', 'population','yearly_p_change',
                                                    'net_p_change', 'density','land_area',
                                                    'fertility_rate','median_age','urban_pop_percent',
                                                    'world_share','total_c_cases','total_c_deaths',
                                                    'total_c_recovered','active_c_cases','serious_c_cases',
                                                    'c_cases_per_mil','c_deaths_per_mil','total_c_tests'])

    # sorts and places corona data into pop data
    for i in range(len(index_names_c)):
        df_world.loc[df_world['name'] == index_names_c[i], ['links']] = country_links_c[i]
        df_world.loc[df_world['name'] == index_names_c[i], ['total_c_cases']] = total_cases_c[i]
        df_world.loc[df_world['name'] == index_names_c[i], ['total_c_deaths']] = total_deaths_c[i]
        df_world.loc[df_world['name'] == index_names_c[i], ['total_c_recovered']] = total_recovered_c[i]
        df_world.loc[df_world['name'] == index_names_c[i], ['active_c_cases']] = active_cases_c[i]
        df_world.loc[df_world['name'] == index_names_c[i], ['serious_c_cases']] = serious_cases_c[i]
        df_world.loc[df_world['name'] == index_names_c[i], ['c_cases_per_mil']] = cases_per_mil_c[i]
        df_world.loc[df_world['name'] == index_names_c[i], ['c_deaths_per_mil']] = deaths_per_mil_c[i]
        df_world.loc[df_world['name'] == index_names_c[i], ['total_c_tests']] = total_tests_c[i]

    return df_world
    





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