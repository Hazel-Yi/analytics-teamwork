import pandas as pd
from sqlalchemy import create_engine

if __name__ == '__main__':
    reviews_csv = 'bgg-13m-reviews.csv'
    details_csv = 'games_detailed_info.csv'
    Database = create_engine('sqlite:///Database.db')
    chunksize=100000
    print("Creating database...")
    for df in pd.read_csv(reviews_csv, chunksize=chunksize, iterator=True):
        df.drop('comment', axis=1, inplace=True)
        df.columns = ['Other_Index', 'User', 'Rating', 'ID', 'Name']
        df.drop('Other_Index', axis=1, inplace=True)
        print(df.head(1).to_string())
        df.to_sql('Reviews', Database, if_exists='append')

    print("Done.")   
    #df = pd.read_csv(details_csv)
    #df = pd.read_sql_query('SELECT * FROM Reviews WHERE User="s-man"', Database)
    #print(df.to_string())
