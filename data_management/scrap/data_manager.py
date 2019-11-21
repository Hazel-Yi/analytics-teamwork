import pandas as pd
import sqlite3
import json
import ast
import os
import sys

class DataManager:

    def __init__(self, root_dir='.'):
        #self.db_fn = os.path.join(root_dir, 'Database.db')
        self.placeholder_img_url = 'https://via.placeholder.com/150x150?text=No+Image'
        self.details_listcat = ['Publisher', 'Category', 'Expansion', 'Mechanic']
        #self._init_db()

    # Get row entries of dataframe, starting from a row index num_rows and extending for
    # num_rows. Output can be either in JSON or dict. All numpy NaN and NA values are converted to
    # null / None. A list of dataframe column names can be provided to interpret each element under 
    # that column as a list.
    def get_json_entries(self, df, start_pos=None, num_rows=None, to_json=True, keyval_list=[]):
        if start_pos == None:
            start_pos = 0
        end_pos = len(df.index) if (num_rows == None) else min(start_pos + num_rows, len(df.index))
        selected = df.iloc[start_pos : end_pos].replace({pd.np.nan: None})
        # all remaining NaN values to be converted to None (client is pure Python)
        # all specified keys to interpret their vals as Python lists (if not None)
        if to_json:
            return selected.to_json(orient='records')

        row_entries = selected.to_dict(orient='records')
        if len(keyval_list) > 0:
            for i in range(len(row_entries)): # row
                for key in keyval_list: # specified column (key)
                    if row_entries[i][key] != None: # null or list
                        row_entries[i][key] = ast.literal_eval(row_entries[i][key])
        return row_entries

    # [NO LONGER USED] :c
    #
    # def getBoardGames(self, start_pos=None, num_rows=None, to_json=True):
    #     return self.get_json_entries(self.games, start_pos, num_rows, to_json)

    # def getBoardGameDetails(self, game_id, to_json=True):
    #     row = self.details[self.details['ID']==game_id]
    #     res_dict = self.get_json_entries(row, 0, 1, False, self.details_listcat)[0]
    #     if to_json: # list wrapper removed
    #         return json.dumps(res_dict)
    #     return res_dict

    # def getBoardGameReviews(self, game_id, to_json=True):
    #     try: # data sanitisation
    #         game_id = int(game_id)
    #         df = pd.read_sql_query('SELECT * FROM Reviews WHERE ID={}'.format(game_id), self.db_conn)
    #         df = df.drop('index', axis=1)
    #         return self.get_json_entries(df, None, None, to_json)
    #     except ValueError:
    #         print("getBoardGameReviews() failed: game id not an integer")
    #     if to_json:
    #         return "{}"
    #     else:
    #         return {}

    # def _init_db(self):
    #     if not os.path.exists(self.db_fn):
    #         print("Missing database: {}".format(self.db_fn))
    #         sys.exit(0)
    #     self.db_conn = sqlite3.connect(self.db_fn)

    # [OLD CSV CODE]
    #
    # def _init_games(self):
    #     self.games = pd.read_csv(self.games_fn)
    #     self.games = self.games.drop(columns=['Bayes average', 'URL'])
    #     # handle any NaN values that don't affect the ML model
    #     self.games['Thumbnail'] = self.games['Thumbnail'].fillna(self.placeholder_img_url)

    # def _init_details(self):
    #     self.details = pd.read_csv(self.details_fn)
    #     self.details = self.details[['id','primary','boardgamepublisher','boardgamecategory','minplayers','maxplayers','minage','minplaytime','description','boardgameexpansion','boardgamemechanic','image', 'yearpublished']]
    #     self.details.columns = ['ID','Name',   'Publisher',         'Category',         'Min players','Max players','Min age','Min playtime','Description','Expansion',     'Mechanic',         'Thumbnail', 'Year Published']
    #     # handle any NaN values that don't affect the ML model
    #     self.details['Thumbnail'] = self.details['Thumbnail'].fillna(self.placeholder_img_url)
    #     self.details_listcat = ['Publisher', 'Category', 'Expansion', 'Mechanic']
