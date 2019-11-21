import sqlite3
import json
import ast
import pandas as pd
from flask import Flask, request
from flask_restplus import Resource, Api, fields, inputs
from data_management import metadata_manager
from Create_db import create_connection

app = Flask(__name__)
api = Api(app, version='1.5', default="Board Game Geek", title="Board Game Geek", description="...")

mm = metadata_manager.MetaDataManager()

# Get row entries of dataframe, starting from a row index num_rows and extending for
# num_rows. Output can be either in JSON or dict. All numpy NaN and NA values are converted to
# null / None. A list of dataframe column names can be provided to interpret each element under 
# that column as a list.
def get_json_entries(df, start_pos=None, num_rows=None, to_json=True, keyval_list=[]):
    if start_pos == None:
        start_pos = 0
    end_pos = len(df.index) if (num_rows == None) else min(start_pos + num_rows, len(df.index))
    selected = df.iloc[start_pos : end_pos].replace({pd.np.nan: None})
    # all remaining NaN values to be converted to None (client is pure Python)
    # all specified keys to interpret their vals as Python lists (if not None)
    row_entries = selected.to_dict(orient='records')
    if len(keyval_list) > 0: # necessary for json output as well
        for i in range(len(row_entries)): # row
            for key in keyval_list: # specified column (key)
                if row_entries[i][key] != None: # null or list
                    row_entries[i][key] = ast.literal_eval(row_entries[i][key])
    return row_entries


review_model = api.model('Review', {
    'Game_ID': fields.Integer,
    'User': fields.String,
    'Rating': fields.Float,
    'Comment': fields.String,
})

detail_model = api.model('Detail', {
    'Game_ID': fields.Integer,
    'Name': fields.String,
    'Publisher': fields.List(fields.String),
    'Category': fields.List(fields.String),
    'Min_players': fields.Integer,
    'Max_players': fields.Integer,
    'Min_age': fields.Integer,
    'Min_playtime': fields.Integer,
    'Description': fields.String,
    'Expansion': fields.List(fields.String),
    'Mechanic': fields.List(fields.String),
    'Thumbnail': fields.Url, ###
    'Year_Published': fields.Integer
})

game_model = api.model('Game', {
    'Game_ID': fields.Integer,
    'Name': fields.String,
    'Year': fields.Integer,
    'Rank': fields.Integer,
    'Average': fields.Float,
    'Bayes_Average': fields.Float,
    'Users_Rated': fields.Integer,
    'URL': fields.Url, ###
    'Thumbnail': fields.Url ###
})

@api.route('/details')
class Board_Games_Details_List(Resource):
    @api.response(200, 'Successful')
    @api.doc(description='Get all board games details')
    ###GET GAMES DETAILS###
    def get(self):
        conn = create_connection('Database')
        df = pd.read_sql_query("SELECT * FROM Details", conn)  ### Chunk this to be loaded onto multiple pages
        mm.increment('/board_games_details')
        return dm.get_json_entries(df, None, None, False)

    ###POST###
    @api.response(201, 'Board Game Details Added Successfully')
    @api.response(400, 'Validation Error')
    @api.doc(description="Add new board game details")
    @api.expect(detail_model, validate=True)
    def post(self):
        details = request.json
        for key in details:
            if key not in detail_model.keys():
                return {"message": "Property {} is invalid".format(key)}, 400

        conn = create_connection('Database')
        c = conn.cursor()
        c.execute("INSERT INTO Details(Game_ID, Name, Publisher, Category, Min_players, Max_players, Min_age, Min_playtime, Description, Expansion, Mechanic, Thumbnail, Year_Published) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (details['Game_ID'],
                details['Name'],
                str(details['Publisher']),
                str(details['Category']),
                details['Min_players'],
                details['Max_players'],
                details['Min_age'],
                details['Min_playtime'],
                details['Description'],
                str(details['Expansion']),
                str(details['Mechanic']),
                details['Thumbnail'],
                details['Year_Published']))
        conn.commit()
        mm.increment('/board_games_details/POST {}'.format(id))
        return {"message": "Game {} is created with ID {}".format(details['Name'], details['Game_ID'])}, 201

###GET API STATS###
@api.route('/api_usage')
class Api_Usage(Resource):
    @api.response(200, 'Successful')
    @api.doc(description='Get Api Usage Stats')
    def get(self):
        api_usage = mm.metadata
        mm.increment('/api_usage')
        return api_usage, 200

@api.route('/details/<int:id>')
@api.param('id', 'Game ID')
class Board_Games(Resource):
    @api.response(404, 'Game not found')
    @api.response(200, 'Successful')
    @api.doc(description="Get a game details by its ID")
    ###GET GAME BY ID###
    def get(self, id):
        conn = create_connection('Database')
        df = pd.read_sql_query("SELECT * FROM Details WHERE Game_ID = {};".format(id), conn)
        if len(df) == 0:
            api.abort(404, "Game {} doesn't exist".format(id))
        details = df.loc[0].to_json()
        details = json.loads(details)
   
        
        mm.increment('/board_games_details/{}'.format(id))
        return details, 200


    @api.response(404, 'Game not found')
    @api.response(400, 'Validation Error')
    @api.response(200, 'Successful')
    @api.expect(detail_model)
    @api.doc(description="Update a game details by its ID")
    ###UPDATE###
    def put(self, id):
        details = request.json
        conn = create_connection('Database')
        c = conn.cursor()
        print("SELECT Detail_ID FROM Details WHERE Game_ID = {}".format(id))
        df = pd.read_sql_query("SELECT Detail_ID FROM Details WHERE Game_ID = {}".format(id), conn)
        index = df.loc[0][0]
        

        for key in details:
            if key not in detail_model.keys():
                return {"message": "Property {} is invalid".format(key)}, 400

        c.execute('UPDATE Details SET Name=?, Publisher=?, Category=?, Min_players=?, Max_players=?, Min_age=?, Min_playtime=?, Description=?, Expansion=?, Mechanic=?, Thumbnail=?, Year_Published=? WHERE Detail_ID=?;', (
                str(details['Name']),
                str(details['Publisher']),
                str(details['Category']),
                details['Min_players'],
                details['Max_players'],
                details['Min_age'],
                details['Min_playtime'],
                str(details['Description']),
                str(details['Expansion']),
                str(details['Mechanic']),
                str(details['Thumbnail']),
                details['Year_Published'],
                int(index)))

        conn.commit()
        mm.increment('/board_games_details/PUT {}'.format(id))

        return {"message": "Game {} has been successfully updated".format(id)}, 200

@api.route('/reviews')
class addReviews(Resource):
    @api.response(201, 'Review Added Successfully')
    @api.response(400, 'Validation Error')
    @api.doc(description="Add a new review")
    @api.expect(review_model, validate=True)
    def post(self):
        review = request.json

        for key in review:
            if key not in review_model.keys():
                return {"message": "Property {} is invalid".format(key)}, 400

        conn = create_connection('Database')
        df = pd.read_sql_query("SELECT Name FROM Games WHERE ID = {};".format(review['Game_ID']), conn)
        if len(df) == 0:
            api.abort(404, "Game {} doesn't exist".format(review['Game_ID']))
        Name = df.loc[0][0]
        c = conn.cursor()
        c.execute("INSERT INTO Reviews(User, Rating, Game_ID, Comment, Name) VALUES(?,?,?,?,?)", (review['User'], review['Rating'], review['Game_ID'], review['Comment'], Name))
        last_row = c.lastrowid
        conn.commit()
        mm.increment('/reviews/POST {}'.format(id))
        return {"message": "Review for game '{}' has been added with ID {}".format(Name, last_row)}, 201




@api.route('/reviews/<int:id>')
@api.param('id', 'Review ID')
class Reviews(Resource):
    @api.response(404, 'Review not found')
    @api.response(200, 'Successful')
    @api.doc(description="Get a Review by its ID")
    ###GET REVIEW BY ID###
    def get(self, id):
        conn = create_connection('Database')
        df = pd.read_sql_query("SELECT * FROM Reviews WHERE Review_ID = {};".format(id), conn)
        if len(df) == 0:
            api.abort(404, "Review {} doesn't exist".format(id))
        review = df.loc[0].to_json()
        review = json.loads(review)
        mm.increment('/review/{}'.format(id))
        if not review:
            api.abort(404, "Review {} doesn't exist".format(id))
        return review, 200


if __name__ == '__main__':

    app.run(host = '127.0.0.1', port = 8000, debug=True)

    
