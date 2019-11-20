import pandas as pd
from sqlalchemy import create_engine
import sqlite3
import os

create_table_Reviews = """ CREATE TABLE IF NOT EXISTS Reviews (ReviewID integer PRIMARY KEY, user text, rating real, comment text, ID integer, name text); """

def create_connection(db_file):
    if not os.path.exists(db_file +'.db'):
        print('Connection failed: ' + db_file +' doesn\'t exist')
        return
    try:
        conn = sqlite3.connect(db_file+'.db')
        print('Connected to ' + db_file +'.db')
    except Exception as e:
        print(e)
    return conn

def create_database(dataframe, db_file):
    if os.path.exists(db_file +'.db'):
        print(db_file +'.db already exists')
        return

    Database = create_engine('sqlite:///{}.db'.format(db_file))
    #conn = sqlite3.connect(db_file+'.db')
    #c = conn.cursor()
    #c.execute(create_table_Reviews)
    chunksize=1000000
    #na_before = 0
    #na_after = 0
    print("Creating database...")
    for df in pd.read_csv(dataframe, chunksize=chunksize, iterator=True):
        df = df[['user', 'rating', 'comment', 'ID', 'name']]
        #na_before += df.isna().sum()
        #df = df.fillna(None)
        #na_after +=df.isna().sum()
        df.to_sql('Reviews', Database, if_exists='append')
        print(df.tail(1).to_string())
    print("Done.")
    #print('NA Before: ' + str(na_before))
    #print('NA After: ' + str(na_after))




if __name__ == '__main__':
    reviews_csv = 'bgg-13m-reviews.csv'
    create_database(reviews_csv, 'Database')
    #create_database(reviews_csv, 'Database2')

    #conn = create_connection('Database')
    #conn2 = create_connection('data')

    #df1 = pd.read_sql_query('SELECT COUNT(*) as Count FROM Reviews', conn)
    #df = df1.loc[0, 'Count']
    #print('Records in Database.db:\t' + str(df))

    #df2 = pd.read_sql_query('SELECT COUNT(*) as Count FROM Reviews', conn2)
    #df = df2.loc[0, 'Count']
    #print('Records in data.db:\t' + str(df))

    #df = pd.read_sql_query('SELECT * FROM Reviews WHERE User="s-man"', conn)

    #df = pd.read_sql_query('PRAGMA table_info(Reviews)', conn)

    #df = pd.read_sql_query('PRAGMA index_list(Reviews)', conn)

    #print(df.to_string())


    
    
    
