import pandas as pd
from sqlalchemy import create_engine
import sqlite3
import os


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


def create_database(db_file):
    if os.path.exists(db_file +'.db'):
        print(db_file +'.db already exists')
        return
    conn = sqlite3.connect(db_file+'.db')
    print(db_file +'.db Created.')
    return conn


def create_table_reviews(dataframe, conn):
    #Index_2 integer,
    create_table_Reviews = ('CREATE TABLE IF NOT EXISTS Reviews (Review_ID integer PRIMARY KEY, Game_ID integer, User text, Rating real, Comment text, Name text);')
    c = conn.cursor()
    print("Creating Table 'Reviews'...")
    try:
        c.execute('DROP TABLE Reviews;')
        print('Overwriting...')
    except:
        pass
    c.execute(create_table_Reviews)
    for df in pd.read_csv(dataframe, chunksize=1000000, iterator=True):
        df.rename(columns ={'user':'User', 'rating':'Rating', 'comment':'Comment', 'ID':'Game_ID', 'name':'Name'}, inplace=True)
        df.drop('Unnamed: 0', axis=1, inplace=True)
        df.to_sql('Reviews', conn, if_exists='append', index=True, index_label='Review_ID')
        print(df.tail(1).to_string())
    print("Done.")


def create_table_games(dataframe, conn):
    create_table_Games = ('CREATE TABLE IF NOT EXISTS Games (Game_ID integer, Name text, Year integer, Rank integer, Average real, Bayes_Average real, Users_Rated integer, URL text, Thumbnail text);')
    c = conn.cursor()
    print("Creating Table 'Games'...")
    try:
        c.execute('DROP TABLE Games;')
        print('Overwriting...')
    except:
        pass
    c.execute(create_table_Games)
    df = pd.read_csv(dataframe)
    df.rename(columns ={'ID':'Game_ID', 'Bayes average':'Bayes_Average', 'Users rated':'Users_Rated'}, inplace=True)
    df.set_index('Game_ID', inplace=True)
    df.to_sql('Games', conn, if_exists='append', index=True)
    print("Done.")


def create_table_details(dataframe, conn):
    create_table_Details = ('CREATE TABLE IF NOT EXISTS Details (Detail_ID integer PRIMARY KEY, Game_ID integer, Name text, Publisher text, Category text, Min_players integer, Max_players integer, Min_age integer, Min_playtime integer, Description text, Expansion text, Mechanic text, Thumbnail text, Year_Published integer);')
    c = conn.cursor()
    print("Creating Table 'Details'...")
    try:
        c.execute('DROP TABLE Details;')
        print('Overwriting...')
    except:
        pass
    c.execute(create_table_Details)
    df = pd.read_csv(dataframe)
    df.rename(columns ={
            'id': 'Game_ID',
            'primary': 'Name',
            'boardgamepublisher': 'Publisher',
            'boardgamecategory': 'Category',
            'minplayers': 'Min_players',
            'maxplayers': 'Max_players',
            'minage': 'Min_age',
            'minplaytime': 'Min_playtime',
            'description': 'Description',
            'boardgameexpansion': 'Expansion',
            'boardgamemechanic': 'Mechanic',
            'image': 'Thumbnail',
            'yearpublished': 'Year_Published'
        }, inplace=True)
    df = df[[
            'Game_ID',
            'Name',
            'Publisher',
            'Category',
            'Min_players',
            'Max_players',
            'Min_age',
            'Min_playtime',
            'Description',
            'Expansion',
            'Mechanic',
            'Thumbnail',
            'Year_Published']]
    df.to_sql('Details', conn, if_exists='append', index=True, index_label='Detail_ID')
    print("Done.")


if __name__ == '__main__':
    reviews_csv = 'bgg-13m-reviews.csv'
    games_csv = '2019-05-02.csv'
    details_csv = 'games_detailed_info.csv'
    conn = create_database('Database')
    create_table_reviews(reviews_csv, conn)
    create_table_games(games_csv, conn)
    create_table_details(details_csv, conn)
