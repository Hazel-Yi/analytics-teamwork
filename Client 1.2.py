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
    #'ID': fields.Integer,
    'Name': fields.String,
    'Publisher': fields.List(fields.String),
    'Category': fields.List(fields.String),
    'Min players': fields.Integer,
    'Max players': fields.Integer,
    'Min age': fields.Integer,
    'Min playtime': fields.Integer,
    'Description': fields.String,
    'Expansion': fields.List(fields.String),
    'Mechanic': fields.List(fields.String),
    'Thumbnail': fields.Url,
    'Year Published': fields.Integer
})



@api.route('/games')
class Board_Games_List(Resource):
    @api.response(200, 'Successful')
    @api.doc(description='Get all board games')
    ###GET GAMES DETAILS###
    def get(self):
        mm.increment('/board_game')
        return dm.get_json_entries(dm.details, None, None, False)

    ###POST NEW GAME (onto copy df)###
    @api.response(201, 'Board Game Added Successfully')
    @api.response(400, 'Validation Error')
    @api.doc(description="Add a new board game")
    @api.expect(detail_model, validate=True)
    def post(self):
        game = request.json
        id = df_details.index[-1] + 1

        if id in df_details.index:
            return {"message": "A game with ID={} is already in the dataset".format(id)}, 400

        for key in game:
            if key not in detail_model.keys():
                return {"message": "Property {} is invalid".format(key)}, 400

        df_details.loc[id, 'ID'] = id

        for key in game:
            df_details.loc[id, key] = game[key]

        return {"message": "Game {} is created with ID {}".format(game['Name'], id)}, 201

###GET API STATS###
@api.route('/api_usage')
class Api_Usage(Resource):
    @api.response(200, 'Successful')
    @api.doc(description='Get Api Usage Stats')
    def get(self):
        api_usage = mm.metadata
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
        mm.increment('/board_game/POST {}'.format(id))
        if not game_row:
            api.abort(404, "Game {} doesn't exist".format(id))
        return game_row


    @api.response(404, 'Game not found')
    @api.response(400, 'Validation Error')
    @api.response(200, 'Successful')
    @api.expect(detail_model)
    @api.doc(description="Update a game by its ID")
    ###UPDATE (onto copy df)###
    def put(self, id):

        #if id not in df_details.index:
            #api.abort(404, "Game {} doesn't exist".format(id))

        game = request.json

        for key in game:
            if key not in detail_model.keys():
                return {"message": "Property {} is invalid".format(key)}, 400

        for key in game:
            df_details.loc[id, key] = game[key]

        return {"message": "Game {} has been successfully updated".format(id)}, 200



if __name__ == '__main__':

    df_games = dm.get_json_entries(dm.games, None, None, False)
    df_details = dm.details

    #print(df_details.dtypes)
    #df_details = df_details.infer_objects()
    #print(df_details.dtypes)

    app.run(debug=True)
