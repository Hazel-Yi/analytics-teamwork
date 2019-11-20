import sqlite3
import json
import pandas as pd
from flask import Flask, request
from flask_restplus import Resource, Api, fields, inputs, reqparse
from data_management import data_manager, metadata_manager

app = Flask(__name__)
api = Api(app, version='1.2', default="Board Game Geek", title="Board Game Geek", description="...")

dm = data_manager.DataManager()
mm = metadata_manager.MetaDataManager()

review_model = api.model('Review', {
    'Index': fields.Integer,
    'User': fields.String,
    'Rating': fields.Float,
    'ID': fields.Integer,
    'Name': fields.String
})


detail_model = api.model('Detail', {
    'id': fields.Integer,
    'primary': fields.String,
    'boardgamepublisher': fields.List(fields.String),
    'boardgamecategory': fields.List(fields.String),
    'minplayers': fields.Integer,
    'maxplayers': fields.Integer,
    'minage': fields.Integer,
    'minplaytime': fields.Integer,
    'description': fields.String,
    'boardgameexpansion': fields.List(fields.String),
    'boardgamemechanic': fields.List(fields.String),
    'image': fields.String,
    'yearpublished': fields.Integer
})


@api.route('/games')
class Board_Games_List(Resource):
    @api.response(200, 'Successful')
    @api.doc(description='Get all board games')
    ###GET GAMES DETAILS###
    def get(self):
        mm.increment('/board_game')
        return dm.get_json_entries(dm.details, None, None, False)


    ###POST###
    @api.response(201, 'Board Game Added Successfully')
    @api.response(400, 'Validation Error')
    @api.doc(description="Add a new board game")
    @api.expect(detail_model, validate=True)
    def post(self):
        #df_details_POST = pd.read_csv('games_detailed_info.csv')
        game = request.json
        id = df_details_POST.index[-1] + 1

        for key in game:
            if key not in detail_model.keys():
                return {"message": "Property {} is invalid".format(key)}, 400

        df_details_POST.loc[id, 'index'] = id

        for key in game:
            df_details_POST.loc[id, key] = game[key]
        df_details_POST.to_csv('games_detailed_info.csv')
        mm.increment('/board_game/POST {}'.format(id))
        return {"message": "Game {} is created with ID {}".format(game['primary'], game['id'])}, 201

###GET API STATS###
@api.route('/api_usage')
class Api_Usage(Resource):
    @api.response(200, 'Successful')
    @api.doc(description='Get Api Usage Stats')
    def get(self):
        api_usage = mm.metadata
        mm.increment('/api_usage')
        return api_usage

@api.route('/games/<int:id>')
@api.param('id', 'Game ID')
class Board_Games(Resource):
    @api.response(404, 'Game not found')
    @api.response(200, 'Successful')
    @api.doc(description="Get a game by its ID")
    ###GET GAME BY ID###
    def get(self, id):
        game = df_details.loc[df_details['ID'] == id]
        game_row = dm.get_json_entries(game, 0, 1, False)[0]
        
        if not game_row:
            api.abort(404, "Game {} doesn't exist".format(id))
        
        mm.increment('/board_game/{}'.format(id))
        return game_row


    @api.response(404, 'Game not found')
    @api.response(400, 'Validation Error')
    @api.response(200, 'Successful')
    @api.expect(detail_model)
    @api.doc(description="Update a game by its ID")
    ###UPDATE###
    def put(self, id):
        game_id = df_details.loc[df_details['ID'] == id].index[0]
        game = request.json
        for key in game:
            if key not in detail_model.keys():
                return {"message": "Property {} is invalid".format(key)}, 400

        for key in game:
            df_details_POST.loc[int(game_id), key] = game[key]

        df_details_POST.to_csv('games_detailed_info.csv')
        mm.increment('/board_game/PUT {}'.format(id))

        return {"message": "Game {} has been successfully updated".format(id)}, 200



if __name__ == '__main__':

    df_games = dm.get_json_entries(dm.games, None, None, False)
    df_details = dm.details

    df_details_POST = pd.read_csv('games_detailed_info.csv')
    df_details_POST.rename(columns ={'Unnamed: 0' : 'index'}, inplace=True)
    #game_id = df_details.loc[df_details['ID'] == 100000].index[0]
    #print(type(int(game_id)))

    app.run(host = '127.0.0.1', port = 8000, debug=True)
    
    
    
    #id = df.index[-1] + 1
    #index = df[df.columns[0]].index[-1] + 1
    #print(id, index)
    #print(df.tail(1))
    #print(df['Unnamed: 0'])
    #print(df.iloc[:,0])
    #print(df.tail(1))
    #df.loc[id, 0] = 123
    #print(df.iloc[17062][0])
    #df.insert(id, 1, str(index), allow_duplicates = False)
    #df_details2 = dm2.getDetails()
    #df = pd.DataFrame(df_details2)
    #df = pd.read_csv('games_detailed_info.csv')
    #df = df[df.columns[0]].index[-1] + 1
    #print(df)
    #print(df_details.dtypes)
    #df_details = df_details.infer_objects()
    #print(df.dtypes)
    #print(df_details.dtypes)

    
