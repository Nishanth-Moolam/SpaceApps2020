import pandas as pd 
import sqlite3

#https://www.youtube.com/watch?v=AtBZC9F-MjI&list=PLQVvvaa0QuDe8XSftW-RAxdo6OmaeL85M&index=68
#https://www.youtube.com/watch?v=vmEHCJofslg
#https://www.youtube.com/watch?v=u5AYFuucvoU


def connect():
    con = sqlite3.connect('test.db')
    c = con.cursor()

# sql commands
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS test(name TEXT, population REAL)')

def data_entry():
    c.execute("INSERT INTO test VALUES('city name', 1000)")
    con.commit()

def read_from_db():
    c.execute('SELECT * FROM test')
    for row in c.fetchall():
        print (row)

def read_high_pop():
    c.execute('SELECT * FROM test WHERE population > 500')
    for row in c.fetchall():
        print (row)

def close_con():
    c.close()
    con.close()

#create_table()
#data_entry()
# read_from_db()
# print ('')
# read_high_pop()
# close_con()


# pandas
con = sqlite3.connect('test.db')
sql = '''
SELECT * FROM test
'''

df = pd.read_sql_query(sql,con)
print (df)
