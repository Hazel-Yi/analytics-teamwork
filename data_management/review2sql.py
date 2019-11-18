import pandas as pd
import time
import os

print("Starting...")
root_dir = '..'
games_fn = os.path.join(root_dir, '2019-05-02.csv')
details_fn = os.path.join(root_dir, 'games_detailed_info.csv')
reviews_fn = os.path.join(root_dir, 'bgg-13m-reviews.csv')

start = time.time()
df = pd.read_csv(reviews_fn)
print("Took {} seconds\r\n".format(time.time() - start))
print(df)