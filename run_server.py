from data_management import data_manager

import pprint
pp = pprint.PrettyPrinter(indent=4)

# just some dummy data management test here at the moment
dm = data_manager.DataManager('.')
print("Games dataframe:")
print(dm.games)
print("Details dataframe:")
print(dm.details)
print("Reviews dataframe:")
print(None) # TODO

print("\r\nTesting: GET /board_game")
pp.pprint(dm.getBoardGames(1,2,False))

print("\r\nTesting: GET /board_game/id")
pp.pprint(dm.getBoardGameDetails(161936,False))