import pandas as pd
import json
from Create_db import create_connection


def generate_review_rating_quantiles(conn):
    sql = '''
select Year, Rating 
from (select Game_ID, Year_Published as Year from Details) natural join 
(select Game_ID, Rating from Reviews) 
order by Year asc;'''
    print("Processing reviews in SQL...")
    df_groups = pd.read_sql_query(sql, conn).groupby('Year')
    print("Generating stats...")
    quantiles = [0,0.25,0.5,0.75,1]
    # quantiles
    res = df_groups.quantile(quantiles[0])
    for i in range(1,len(quantiles)):
         res = res.merge( df_groups.quantile(quantiles[i]), on='Year')
    # average
    res = res.merge( df_groups.mean(), on='Year')
    # count
    res = res.merge( df_groups.count(), on='Year')
    columns = ['Min_Rating', 'Q1_Rating', 'Median_Rating', 'Q3_Rating', 'Max_Rating', 'Average_Rating', 'Num_Ratings']
    res.columns = columns
    res['Year'] = res.index
    print(res)
    return res


if __name__ == '__main__':
    conn = create_connection('Database')
    df_quantiles = generate_review_rating_quantiles(conn)
    with open('review_rating_quantiles.json', 'w') as f:
        f.write(df_quantiles.to_json(orient='records'))