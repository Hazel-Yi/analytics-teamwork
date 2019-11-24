# analytics-teamwork
Assignment for Data Services Engineering 2019

## Dataset Sources

The board games information is sourced from Kaggle: https://www.kaggle.com/jvanelteren/boardgamegeek-reviews

Pricing information is webscrapped from https://www.boardgamegateway.com/ and https://www.amazon.com (US and AU).

## Setup Instructions

Make sure you have (at least) the following installed:

 * Python 3
 * Flask and Flask RESTPlus
 * pandas
 * sqlite3
 * Jupyter Notebook

To initialise the sqlite3 database, please run the following commands:

```
python Create_db.py
python gen_review_stats.py
```

The cached results of the machine learning model for performing board game recommendations is stored in `recommendations.json`. This should already be provided in the repository. However, if you would like to re-generate this data source, this can be done by opening a new session of `jupyter notebook` and doing Cell > Run All on the `BoardGames.ipynb` notebook.


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

## Link to trained model
https://drive.google.com/file/d/1kfv4QfATkuh3atbocB9nfHJLdBk-fptI/view?usp=sharing

