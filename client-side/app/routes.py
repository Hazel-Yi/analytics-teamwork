from flask import Flask, render_template, request
import requests
from app import app
import json

@app.route('/')
@app.route('/get_top10')
def get_top10():
  r = requests.get("http://127.0.0.1:8000/details/top10", params={'order': 'Game_ID', 'ascending':True})
  games = r.json()

  '''testing = games[1]
  print(testing)'''

  listlist = []
  game_id_list = []
  name_list = []
  year_list = []

  for game in games:
    sublist = []
    for key in game.keys():
      if key == 'Game_ID':
        game_id = str(game[key])
        game_id_list.append(game_id)
      if key == 'Name':
        name = str(game[key])
        name_list.append(name)
      if key == 'Year_Published':
        year = str(game[key])
        year_list.append(year) 
    sublist.append(game_id)
    sublist.append(name)
    sublist.append(year)
    listlist.append(sublist)

  '''print(listlist[0])'''

  return render_template('get_top10.html', title='Popular Boardgames', listlist=listlist)

@app.route('/get_boardgame')
def get_boardgame():
  r = requests.get("http://127.0.0.1:8000/details", params={'order': 'Game_ID', 'ascending':True})
  games = r.json()

  '''testing = games[1]
  print(testing)'''

  listlist = []
  game_id_list = []
  name_list = []
  year_list = []

  for game in games:
    sublist = []
    for key in game.keys():
      if key == 'Game_ID':
        game_id = str(game[key])
        game_id_list.append(game_id)
      if key == 'Name':
        name = str(game[key])
        name_list.append(name)
      if key == 'Year_Published':
        year = str(game[key])
        year_list.append(year)  
    sublist.append(game_id)
    sublist.append(name)
    sublist.append(year)
    listlist.append(sublist)

  '''print(listlist[0])'''

  return render_template('get_boardgame.html', title='All Boardgames', listlist=listlist)
    

@app.route('/get_boardgame_id', methods=['GET', 'POST'])
def get_boardgame_id():
  if request.method == 'POST':
    search_id = request.form['search']
    print("searched for a game with id " + search_id) 
    r = requests.get("http://127.0.0.1:8000/details/" + str(search_id))
    game = r.json()
    for key in game.keys():
      if key == 'Name':
        name = str(game[key])
      if key == 'Publisher':
        published_by = str(game[key])
      if key == 'Category':
        categories = str(game[key])
      if key == 'Description':
        description = str(game[key])
      if key == 'Expansion':
        expansions = str(game[key])
    '''print(name)'''
    return render_template('get_boardgame_id_2.html', title='Find Boardgame', name=name, published_by=published_by, categories=categories, description=description, expansions=expansions)
  else:
    return render_template('get_boardgame_id.html', title='Find Boardgame')

@app.route('/post_boardgame', methods=['GET', 'POST'])
def post_boardgame():
  if request.method == 'POST':
    published_by = []
    categories = []
    expansions = []
    mechanics = []
    board_game_family = []

    game_id = request.form['id']
    name = request.form['name']
    rank = ""
    published_by.append(request.form['published_by'])
    categories.append(request.form['categories'])
    min_players = request.form['min_players']
    max_players = request.form['max_players']
    min_age = request.form['min_age']
    min_playtime = request.form['min_playtime']
    max_playtime = request.form['max_playtime']
    description = request.form['description']
    expansions.append(request.form['expansions'])
    board_game_family.append(request.form['board_game_family'])
    mechanics.append(request.form['mechanics'])
    thumbnail = request.form['thumbnail']
    year = request.form['year']
    '''print(name)'''
    game = {
      'Game_ID': int(game_id),
      'Name': name,
      'Board_Game_Rank': rank,
      'Publisher': published_by,
      'Category': categories,
      'Min_players': int(min_players),
      'Max_players': int(max_players),
      'Min_age': int(min_age),
      'Min_playtime': int(min_playtime),
      'Max_playtime': int(max_playtime),
      'Description': description,
      'Expansion': expansions,
      'Board_Game_Family': board_game_family,
      'Mechanic': mechanics,
      'Thumbnail': thumbnail,
      'Year_Published': int(year)
    }
    print(game)

    auth = requests.get("http://127.0.0.1:8000/auth")
    token = auth.json()

    print(token)
    for key in token.keys():
      t = str(token[key])
      
    print(t)
    
    r = requests.post("http://127.0.0.1:8000/details", json=game, headers={'AUTH-TOKEN': t})

    print("Status Code:" + str(r.status_code))
    resp = r.json()

    print(resp['message'])

  return render_template('post_boardgame.html', title='Add a Boardgame')

@app.route('/put_boardgame', methods=['GET', 'POST'])
def put_boardgame():
  if request.method == 'POST':
    published_by = []
    categories = []
    expansions = []
    mechanics = []
    board_game_family = []
    game_id = request.form['id']
    name = request.form['name']
    published_by.append(request.form['published_by'])
    categories.append(request.form['categories'])
    min_players = request.form['min_players']
    max_players = request.form['max_players']
    min_age = request.form['min_age']
    min_playtime = request.form['min_playtime']
    max_playtime = request.form['max_playtime']
    description = request.form['description']
    expansions.append(request.form['expansions'])
    board_game_family.append(request.form['board_game_family'])
    mechanics.append(request.form['mechanics'])
    thumbnail = request.form['thumbnail']
    year = request.form['year']
    
    game = {
      'Game_ID': int(game_id),
      'Name': name,
      'Publisher': published_by,
      'Category': categories,
      'Min_players': int(min_players),
      'Max_players': int(max_players),
      'Min_age': int(min_age),
      'Min_playtime': int(min_playtime),
      'Max_playtime': int(max_playtime),
      'Description': description,
      'Expansion': expansions,
      'Board_Game_Family': board_game_family,
      'Mechanic': mechanics,
      'Thumbnail': thumbnail,
      'Year_Published': int(year)
    }

    r = requests.get("http://127.0.0.1:8s000/details/" + str(game_id))
    searched_game = r.json()

    for key in searched_game.keys():
      if key == 'Name':
        if str(searched_game[key]) == name:
          print("okay")
        else:
          print("not okay")

    print("searched for a game with id " + game_id)

    print(game)

    auth = requests.get("http://127.0.0.1:8000/auth")
    token = auth.json()

    print(token)
    for key in token.keys():
      t = str(token[key])
      
    print(t)

    '''print(searched_game)

    r = requests.put("http://127.0.0.1:8000/details/" + str(game_id), headers={'AUTH-TOKEN': t})
    game = r.json()
    print(game)'''

  return render_template('put_boardgame.html', title='Update a Boardgame')

@app.route('/get_rec', methods=['GET', 'POST'])
def get_rec():
  '''get 30 recommended games provided by the ML model'''
  if request.method == 'POST':
    search_id = request.form['search']
    num_rec = int(request.form['num_rec'])

    r = requests.get("http://127.0.0.1:8000/recommendations/" + str(search_id))
    games = r.json()

    rec = games[0:num_rec]

    '''print(games[0])'''

    return render_template('get_rec_2.html', title='Recommended Games', rec=rec, num_rec=num_rec) 
  else:
    return render_template('get_rec.html', title='Recommended Games')

@app.route('/get_review', methods=['GET', 'POST'])
def get_review():
  if request.method == 'POST':
    search_id = request.form['search']
    print("searched for reviews with game id " + search_id) 
    r = requests.get("http://127.0.0.1:8000/reviews/" + str(search_id))
    reviews = r.json()

    listlist = []
    review_id_list = []
    user_list = []
    rating_list = []
    comment_list = []

    for review in reviews:
      sublist = []
      for key in review.keys():
        if key == 'Review_ID':
          review_id = str(review[key])
          review_id_list.append(review_id)
        if key == 'User':
          user = str(review[key])
          user_list.append(user)
        if key == 'Rating':
          rating = str(review[key])
          rating_list.append(rating)  
        if key == 'Comment':
          comment = str(review[key])
          comment_list.append(comment)  
      sublist.append(review_id)
      sublist.append(user)
      sublist.append(rating)
      sublist.append(comment)
      listlist.append(sublist)
    return render_template('get_review_2.html', title='Find Reviews', listlist=listlist)
  else:
    return render_template('get_review.html', title='Find Reviews')

@app.route('/post_review', methods=['GET', 'POST'])
def post_review():
  if request.method == 'POST':
    game_id = request.form['id']
    username = request.form['username']
    rating = request.form['rating']
    comment = request.form['comment']

    review = {
      'Game_ID': int(game_id),
      'User': username,
      'Rating': float(rating),
      'Comment': comment,
    }
    
    print(review)

    auth = requests.get("http://127.0.0.1:8000/auth")
    token = auth.json()

    print(token)
    for key in token.keys():
      t = str(token[key])
      
    print(t)

    r = requests.post("http://127.0.0.1:8000/reviews", json=review, headers={'AUTH-TOKEN': t})

    print("Status Code:" + str(r.status_code))
    resp = r.json()

    print(resp['message'])
  return render_template('post_review.html', title='Add a Review')