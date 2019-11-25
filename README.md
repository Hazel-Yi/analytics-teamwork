# analytics-teamwork
Assignment for Data Services Engineering 2019

## Dataset Sources

The board games information is sourced from Kaggle: https://www.kaggle.com/jvanelteren/boardgamegeek-reviews

Pricing information is webscrapped from https://www.boardgamegateway.com/ and https://www.amazon.com (US and AU).

## Additional Documentation

The Swagger JSON file and the single page document for the API use cases (`Comp9321 Use Cases.docx`) can both be found in the folder `documentation` under this root directory.

## Setup Instructions

Make sure you have (at least) the following installed:

 * Python 3
 * Flask and Flask RESTPlus and flask-paginate, flask_cors
 * matplotlib
 * pandas
 * sqlite3
 * Jupyter Notebook
 

To initialise the sqlite3 database, please run the following commands:

```
python Create_db.py
```

The cached results of the machine learning model for performing board game recommendations is stored in `recommendations.json`. This should already be provided in the repository. However, if you would like to re-generate this data source, this can be done by opening a new session of `jupyter notebook` and doing Cell > Run All on the `BoardGames.ipynb` notebook.

The cached results for one of the trend endpoints is stored in `review_rating_quantiles.json` (due to the time needed to generate it) and should also already be provided by the repository. If it needs to be re-generated however, please run: `python gen_review_stats.py` from the root directory.


## Runtime Instructions

To run the client (user interface front-end), please run the following commands in a new terminal session (Windows description below) from the root directory:

```
set FLASK_APP=client-side\boardgames.py
flask run
```

To run the server (decoupled, data-only API back-end), please run the following commands in a new terminal session (Windows description below) from the root directory:

```
python API.py
```

### Example Payload for POST /details (requires Auth)
```json
{
  "Game_ID": 99999,
  "Name": "Acquire",
  "Board_Game_Rank": 223,
  "Publisher": "['3M', 'The Avalon Hill Game Co', 'Avalon Hill Games, Inc.', 'Dujardin', 'Grow Jogos e Brinquedos', 'PS-Games', 'Schmidt France', 'Schmidt International', 'Schmidt Spiele', 'Selecta Spel en Hobby', 'Smart Games, Inc.']",
  "Category": ["Economic"],
  "Min_players": 2,
  "Max_players": 6,
  "Min_age": 12,
  "Min_playtime": 90,
  "Max_playtime": 90,
  "Description": "In Acquire, each player strategically invests in businesses, trying to retain a majority of stock.  As the businesses grow with tile placements, they also start merging, giving the majority stockholders of the acquired business sizable bonuses, which can then be used to reinvest into other chains.  All of the investors in the acquired company can then cash in their stocks for current value or trade them 2-for-1 for shares of the newer, larger business.  The game is a race to acquire the greatest wealth.&#10;&#10;This Sid Sackson classic has taken many different forms over the years depending on the publisher.  Some versions of the 3M bookshelf edition included rules for a 2-player variant. The original version is part of the 3M Bookshelf Series.&#10;&#10;Note: many books and websites incorrectly list this as a 1962 publication.&#10;&#10;",
  "Expansion": [],
  "Board_Game_Family": ["3M Bookshelf Series"],
  "Mechanic": "['Hand Management', 'Stock Holding', 'Tile Placement']",
  "Thumbnail": "https://cf.geekdo-images.com/original/img/Bz4tTHNpq6gUKFkJs0fJdVIGR1s=/0x0/pic3299296.jpg",
  "Year_Published": 1964
}
```

## Old link to trained model (for Meeting 1)
https://drive.google.com/file/d/1kfv4QfATkuh3atbocB9nfHJLdBk-fptI/view?usp=sharing

