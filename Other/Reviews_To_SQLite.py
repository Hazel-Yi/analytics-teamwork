import json
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import requests
from flask import Flask, request
from flask_restplus import Resource, Api, fields, inputs, reqparse

app = Flask(__name__)
api = Api(app, version='1.0', default="Board Game Geek", title="Board Game Geek", description="...")


if __name__ == '__main__':
    reviews_csv = 'bgg-13m-reviews.csv'
    details_csv = 'games_detailed_info.csv'
    Database = create_engine('sqlite:///Database.db')
    chunksize=100000
    for df in pd.read_csv(reviews_csv, chunksize=chunksize, iterator=True):
        df.drop('comment', axis=1, inplace=True)
        df.columns = ['Other_Index', 'User', 'Rating', 'ID', 'Name']
        df.drop('Other_Index', axis=1, inplace=True)
        print(df.head(1).to_string())
        df.to_sql('Reviews', Database, if_exists='append')
        
    #df = pd.read_csv(details_csv)

    
    df = pd.read_sql_query('SELECT * FROM Reviews WHERE User="s-man"', Database)
    print(df.to_string())
