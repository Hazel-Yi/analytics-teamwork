from data_management import data_manager, metadata_manager

import pprint
pp = pprint.PrettyPrinter(indent=4)

# just some dummy data management test here at the moment
dm = data_manager.DataManager()
mm = metadata_manager.MetaDataManager()

print("Games dataframe:")
print(dm.games)
print("Details dataframe:")
print(dm.details)
print("Reviews dataframe:")
print(None) # TODO - keep the minimum number of columns needed for ML

print("\r\nTesting: GET /board_game")
pp.pprint(dm.getBoardGames(1,2,False))
mm.increment('/board_game')

print("\r\nTesting: GET /board_game/id")
pp.pprint(dm.getBoardGameDetails(161936,False))
mm.increment('/board_game/{}'.format(161936))

# print("Stuck, waiting for user quit...")
# raise ValueError('Fake error')
# while True:
#     continue