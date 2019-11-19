-- run the following in terminal:
-- sqlite3 data.db
-- .read db_create.sql
--
-- program assumes hardcoded file path of .csv file

BEGIN TRANSACTION;

DROP TABLE IF EXISTS Reviews;
DROP TABLE IF EXISTS ReviewsTemp;

CREATE TABLE Reviews(
    id INTEGER PRIMARY KEY,
    user TEXT,
    rating REAL,
    comment TEXT,
    game_id INTEGER,
    game_name TEXT    
);

-- load .csv file (takes a while)
.import bgg-13m-reviews.csv ReviewsTemp

-- use correct data types
INSERT INTO Reviews("user", "rating", "comment", "game_id", "game_name")
  SELECT "user", "rating", "comment", "ID", "name"
  FROM ReviewsTemp;

DROP TABLE ReviewsTemp;

-- replace any empty strings with null
-- (only occurs in: user, comment)
UPDATE Reviews SET user = NULL WHERE user == "" OR user == "null";
UPDATE Reviews SET comment = NULL WHERE comment == "" OR comment == "null";

-- user: 66 NaN values
-- comment: 10532317 NaN values

COMMIT;