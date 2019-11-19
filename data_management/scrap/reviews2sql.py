import pandas as pd
import time
import os

def print_nan_stat(df):
    for c in df.columns.values:
        vals = df[[c]]
        num_na = int(vals.isna().sum())
        if num_na > 0:
            print('{}: {} NaN values'.format(c, num_na))

# 22 seconds on Victor's laptop
def pd_test_loadtime(fn):
    start = time.time()
    df = pd.read_csv(fn)
    print("Took {} seconds\r\n".format(time.time() - start))
    print(df)
    print("")
    print_nan_stat(df)
    if fn == reviews_fn:
        print(df[df['user'].isna()])

def print_file_head(fn, num_rows):
    with open(fn, 'r') as fo:
        for i in range(num_rows):
            print(fo.readline().strip())


if __name__ == '__main__':
    root_dir = '..'
    games_fn = os.path.join(root_dir, '2019-05-02.csv')
    details_fn = os.path.join(root_dir, 'games_detailed_info.csv')
    reviews_fn = os.path.join(root_dir, 'bgg-13m-reviews.csv')
    print("Starting...\r\n")
    #print_file_head(reviews_fn, 5)
    pd_test_loadtime(reviews_fn)
