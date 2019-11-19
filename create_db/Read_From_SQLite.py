import sqlite3
import json
import pandas as pd
import requests
from flask import Flask, request
from flask_restplus import Resource, Api, fields, inputs, reqparse

app = Flask(__name__)
api = Api(app, version='1.0', default="Board Game Geek", title="Board Game Geek", description="Blah Blah Blah.")

review_model = api.model('Review', {
    'Index': fields.Integer,
    'User': fields.String,
    'Rating': fields.Float,
    'ID': fields.Integer,
    'Name': fields.String
})

detail_model = api.model('Detail', {
    'ID': fields.Integer,
    'Name': fields.String,
    'Publisher': fields.List,
    'Category': fields.List,
    'Min_players': fields.Integer,
    'Max_players': fields.Integer,
    'Min_age': fields.Integer,
    'Min_playtime': fields.Integer,
    'Description': fields.String,
    'Expansion': fields.List,
    'Mechanic': fields.List,
    'Thumbnail': fields.Url
})

if __name__ == '__main__':

    def create_connection(db_file):
        conn = None
        conn = sqlite3.connect(db_file)
        return conn

    Database = create_connection('Database.db')
    df = pd.read_sql_query('SELECT * FROM Reviews WHERE User="s-man"', Database)
    print(df.to_string())
    #df = pd.read_sql_query('SELECT * FROM data', database)
    #print(df.to_string())