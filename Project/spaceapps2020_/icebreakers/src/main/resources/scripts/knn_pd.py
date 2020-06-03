import pandas as pd
import numpy as np
from scipy.spatial import distance
import sqlite3



def make_csv_df(filename):
    '''
    reads csv saves to pandas df
    '''
    with open(filename, 'r') as csvfile:
        df = pd.read_csv(csvfile)
    return df

def make_sql_df(sql,con):
    '''
    reads sql query and returns pandas dataframe
    '''
    df = pd.read_sql_query(sql, con)
    return df

def connect_db(db_name):
    '''
    connects to database, returns connection
    '''
    con = sqlite3.connect(db_name)
    return con

def find_nearest_neighbours(user, df, distance_columns, k):
    '''
    returns a list of length k with nearest neighbours of user in df using distance_columns
    '''
    df_numeric = df[distance_columns]
    df_normalized = (df_numeric - df_numeric.mean()) / df_numeric.std()
    user_normalized = df_normalized[df["name"] == user]
    euclidean_distances = df_normalized.apply(lambda row: distance.euclidean(row, user_normalized), axis=1)
    distance_frame = pd.DataFrame(data={"dist": euclidean_distances, "idx": euclidean_distances.index})
    distance_frame.sort_values("dist", inplace=True)

    neighbours = []
    for i in range(k):
        neighbour = distance_frame.iloc[i+1]["idx"]
        neighbours.append(df.loc[int(neighbour)]['name'])

    return neighbours

df =  make_csv_df('test.csv')
distance_columns = ['personality trait 1', 'personality trait 2', 'personality trait 3',
                    'personality trait 4', 'personality trait 5', 'personality trait 6',]

# prints the 4 closest personalities to alice
print (find_nearest_neighbours('alice', df , distance_columns, 1))

