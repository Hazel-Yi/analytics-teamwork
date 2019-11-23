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
bg = dm.getBoardGames(1,2,False)
#pp.pprint(bg)
mm.increment('/board_game')

print("\r\nTesting: GET /board_game/id")
bgd = dm.getBoardGameDetails(161936,False)
#pp.pprint(bgd)
mm.increment('/board_game/{}'.format(161936))

print("\r\nTesting: GET board game reviews")
bgr = dm.getBoardGameReviews(256999,False)
#pp.pprint(bgr)
#print("\r\nlength:", len(bgr))
mm.increment('/board_game/{}'.format(256999))




print("\r\nTesting: GET /usage")
u = mm.getUsage(False)
#pp.pprint(u)

# print("Stuck, waiting for user quit...")
# raise ValueError('Fake error')
# while True:
#     continue