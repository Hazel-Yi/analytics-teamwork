from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_parameter
import requests
from app import app
import json
import ast

@app.route('/')
@app.route('/get_top10')
def get_top10():
  r = requests.get("http://127.0.0.1:8000/details/top10", params={'order': 'Game_ID', 'ascending':True})
  games = r.json()

  '''testing = games[1]
  print(testing)'''

  listlist = []

  for game in games:
    # sublist = []
    game_item = {}
    for key in game.keys():
      if key == 'Game_ID':
        game_item['ID'] = str(game[key])
      if key == 'Name':
        game_item['Name'] = str(game[key])
      if key == 'Year_Published':
        game_item[key] = str(game[key])
      if key =='Thumbnail':
        game_item[key] = str(game[key])
    listlist.append(game_item)

  '''print(listlist[0])'''

  return render_template('get_top10.html', title='Popular Boardgames', listlist=listlist)

@app.route('/get_boardgame')
def get_boardgame():

  q = request.args.get('q')
  search=False
  print(q)
  if q:
    search = True

  page = request.args.get(get_page_parameter(), type=int, default=1)

  r = requests.get("http://127.0.0.1:8000/details", params={'order': 'Game_ID', 'ascending':True, 'Page':page})
  pagination = Pagination(page=page, total=17605, search=search, record_name='users',css_framework='bootstrap3')
  games = r.json()

  '''testing = games[1]
  print(testing)'''

  listlist = []


  for game in games:
    game_item = {}
    for key in game.keys():
      if key == 'Game_ID':
        game_item['ID'] = str(game[key])
      if key == 'Name':
        game_item['Name'] = str(game[key])
      if key == 'Year_Published':
        game_item[key] = str(game[key])
      if key =='Thumbnail':
        game_item[key] = str(game[key])

    listlist.append(game_item)


  return render_template('get_boardgame.html', title='All Boardgames', listlist=listlist, pagination=pagination)
  

@app.route('/find_boardgame', methods=['GET', 'POST'])
def find_boardgame():
  return render_template('find_boardgame.html', title='Find Boardgame')

@app.route('/get_boardgame_id', methods=['GET', 'POST'])
def get_boardgame_id():
  if request.method == 'POST':
    search_id = request.form['search']
    print("searched for a game with id " + search_id) 
    r = requests.get("http://127.0.0.1:8000/details/" + str(search_id))

    if(r.status_code == 404):
      return render_template('Game404.html', title='Find Boardgame',value=search_id)

    game = r.json()
    for key in game.keys():
      if key == 'Name':
        name = str(game[key])
      if key == 'Publisher':
        published_by = game[key]
      if key == 'Category':
        categories = game[key]
      if key == 'Description':
        description = str(game[key])
      if key == 'Expansion':
        expansions = game[key]
    return render_template('get_boardgame_id_2.html', title='Find Boardgame', name=name, published_by=published_by, categories=categories, description=description, expansions=expansions)
  else:
    return render_template('get_boardgame_id.html', title='Find Boardgame')

@app.route('/get_boardgame_name', methods=['GET', 'POST'])
def get_boardgame_name():
  if request.method == 'POST':
    search_name = request.form['search']
    print("searched for a game with name " + search_name) 
    r = requests.get("http://127.0.0.1:8000/details/" + str(search_name))
    print(r.status_code)

    if(r.status_code == 404):
      return render_template('Game404.html', title='Find Boardgame',value=search_name)

    games = r.json()
    listlist = []
    for game in games:
      game_item = {}
      for key in game.keys():
        if key == 'Name':
          game_item[key] = str(game[key])
        if key == 'Publisher':
          game_item[key] = game[key]
        if key == 'Category':
          game_item[key] = game[key]
        if key == 'Description':
          game_item[key] = str(game[key])
        if key == 'Expansion':
          game_item[key] = game[key]
      listlist.append(game_item)
    
    return render_template('get_boardgame_name_2.html', title='Find Boardgame', listlist=listlist)
  else:
    return render_template('get_boardgame_name.html', title='Find Boardgame')

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
    rank = request.form['board_game_rank']
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

    auth_to_post = {'username':request.form['admin_user'], 'password':request.form['admin_pw']}
    auth = requests.post("http://127.0.0.1:8000/auth", json=auth_to_post)
    token = auth.json()


    print("TOKEN:",token)
    for key in token.keys():
      t = str(token[key])
      
    print(t)
    
    r = requests.post("http://127.0.0.1:8000/details", json=game, headers={'AUTH-TOKEN': t})

    if(r.status_code == 401):
      return render_template('401.html', title='Add a Boardgame')

    print("Status Code:" + str(r.status_code))
    resp = r.json()

    print(resp['message'])

  return render_template('post_boardgame.html', title='Add a Boardgame')


@app.route('/put_boardgame', methods=['GET', 'POST', 'PUT'])
def put_boardgame():
  if request.method == 'POST':
    published_by = []
    categories = []
    expansions = []
    mechanics = []
    board_game_family = []

    game_id = request.form['id']
    name = request.form['name']
    rank = request.form['board_game_rank']
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

    r = requests.get("http://127.0.0.1:8000/details/" + str(game_id))
    searched_game = r.json()

    #print(searched_game)

    if name == "":
      name = str(searched_game['Name'])
    if rank == "":
      rank = str(searched_game['Board_Game_Rank'])
    if published_by[0] == "":
      published_by = []
      published_by.append(searched_game['Publisher'])
    if categories[0] == "":
      categories[0] = searched_game['Category']
    if min_players == "":
      min_players = int(searched_game['Min_players'])
    if max_players == "":
      max_players = int(searched_game['Min_players'])
    if min_age == "":
      min_age = int(searched_game['Min_age'])
    if min_playtime == "":
      min_playtime = int(searched_game['Min_playtime'])
    if max_playtime == "":
      max_playtime = int(searched_game['Max_playtime'])
    if description == "":
      description = str(searched_game['Description'])
    if expansions[0] == "":
      expansions[0] = searched_game['Expansion']
    if board_game_family[0] == "":
      board_game_family[0] = searched_game['Board_Game_Family']
    if mechanics[0] == "":
      mechanics[0] = searched_game['Mechanic']
    if thumbnail == "":
      thumbnail = str(searched_game['Thumbnail'])
    if year == "":
      year = int(searched_game['Year_Published'])

    game = {
      'Game_ID': int(game_id),
      'Name': name,
      'Board_Game_Rank': searched_game['Board_Game_Rank'],
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


    auth_to_post = {'username':request.form['admin_user'], 'password':request.form['admin_pw']}
    auth = requests.post("http://127.0.0.1:8000/auth", json=auth_to_post)
    token = auth.json()
    for key in token.keys():
      t = str(token[key])

    r = requests.put("http://127.0.0.1:8000/details/", json=game, headers={'AUTH-TOKEN': t})
    print(r.status_code)
    
    if(r.status_code == 401):
      return render_template('401.html', title='Update a Boardgame')

    inputgame = r.json()
    print(inputgame)

  return render_template('put_boardgame.html', title='Update a Boardgame')

@app.route('/get_rec', methods=['GET', 'POST'])
def get_rec():
  '''get 30 recommended games provided by the ML model'''
  games = None
  categories = ['Action / Dexterity','Abstract Strategy', 'Adventure', 'Age of Reason', 'American Civil War',  'American Indian Wars', 'American Revolutionary War', 'American West', 
    'Ancient', 'Animals', 'Arabian', 'Aviation / Flight', 'Bluffing', 'Book',  'Card Game', 'Children\'s Game', 'City Building', 'Civil War', 'Civilization',  'Collectible Components',
     'Comic Book / Strip', 'Deduction', 'Dice', 'Economic','Educational', 'Electronic','Environmental','Expansion for Base-game','Exploration','Fan Expansion','Fantasy','Farming','Fighting',
     'Game System','Horror','Humor','Industry / Manufacturing','Korean War','Mafia','Math','Mature / Adult','Maze','Medical','Medieval','Memory','Miniatures','Modern Warfare','Movies / TV / Radio theme',
     'Murder/Mystery','Music','Mythology','Napoleonic','Nautical','Negotiation','Novel-based','Number','Party Game','Pike and Shot','Pirates','Political','Post-Napoleonic','Prehistoric','Print & Play',
     'Puzzle','Racing','Real-time','Religious','Renaissance','Science Fiction','Space Exploration','Spies/Secret Agents','Sports','Territory Building','Trains','Transportation','Travel','Trivia',
     'Video Game Theme','Vietnam War','Wargame','Word Game','World War I','World War II','Zombies']
  if request.method == 'POST':
    print(request.form)
    print(request.form.getlist('category'))
    results = request.form
    # return ('okay')


    query_params = {}

    if (results['search'] != ''):
      query_params['Name'] = results['search']
    if (results['min_players'] != ''):
      query_params['Min_players'] = results['min_players']
    if (results['max_players'] != ''):
      query_params['Max_players'] = results['max_players']
    if (results['min_year'] != ''):
      query_params['Min_Year_Published'] = results['min_year'] 
    if (results['max_year'] != ''):
      query_params['Max_Year_Published'] = results['max_year']
    if (results['min_playtime'] != ''):
      query_params['Min_playtime'] = results['min_playtime']
    if (results['max_playtime'] != ''):
      query_params['Max_Year_Published'] = results['max_playtime']
    if (len(request.form.getlist('category')) != 0):
      query_params['Category'] = str(request.form.getlist('category'))
    print(query_params)

    r = requests.get("http://127.0.0.1:8000/recommendations", params=query_params)
    print(r)
    games = r.json()
    print('results')
    print(games)


    '''print(games[0])'''
  return render_template('get_rec.html', title='Recommended Games', games=games, options=categories)

#     return render_template('get_rec_2.html', title='Recommended Games', rec=rec, num_rec=num_rec) 
#   else:


@app.route('/get_review', methods=['GET', 'POST'])
def get_review():
  if request.method == 'POST':
    search_id = request.form['search']
    print("searched for reviews with game id " + search_id) 
    r = requests.get("http://127.0.0.1:8000/reviews/" + str(search_id))
    
    if(r.status_code == 404):
      return render_template('Review404.html', title='Find Reviews',value=search_id)
    
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

    auth_to_post = {'username':request.form['admin_user'], 'password':request.form['admin_pw']}
    auth = requests.post("http://127.0.0.1:8000/auth", json=auth_to_post)
    token = auth.json()

    print(token)
    for key in token.keys():
      t = str(token[key])
      
    print(t)

    r = requests.post("http://127.0.0.1:8000/reviews", json=review, headers={'AUTH-TOKEN': t})

    print("Status Code:" + str(r.status_code))
    if(r.status_code == 401):
      return render_template('401.html', title='Add a Review')

    resp = r.json()

    print(resp['message'])
  return render_template('post_review.html', title='Add a Review')

@app.route('/num_published')
def num_published():

  ''' for num published '''
  r = requests.get("http://127.0.0.1:8000/trends/num_published")
  trends = r.json()
  trends_subset = trends[-10:]

  '''print(trends_subset)'''

  year_list = []
  num_list = []
  listlist = []

  for trend in trends_subset:
    sublist = []
    for key in trend.keys():
      if key == 'Year':
        year = int(trend[key])
        year_list.append(year)
      if key == 'Number_Published':
        num = int(trend[key])
        num_list.append(num)
    sublist.append(year)
    sublist.append(num)
    listlist.append(sublist)
 
  '''print(year_list)
  print(num_list)
  print(listlist)'''

  ''' for rating stats '''

  r = requests.get("http://127.0.0.1:8000/trends/rating_stats")
  rating_stats = r.json()
  rating_stats_subset = rating_stats[-10:]

  print(rating_stats_subset)

  min_list = []
  q1_list = []
  median_list = []
  q3_list = []
  max_list = []
  average_list = []
  year_list_2 = []
  listlist_2 = []

  for rating_stat in rating_stats_subset:
    sublist = []
    for key in rating_stat.keys():
      if key == 'Min_Rating':
        min_r = int(rating_stat[key])
        min_list.append(min_r)
      if key == 'Q1_Rating':
        q1 = int(rating_stat[key])
        q1_list.append(q1)
      if key == 'Median_Rating':
        med = int(rating_stat[key])
        median_list.append(med)
      if key == 'Q3_Rating':
        q3 = int(rating_stat[key])
        q3_list.append(q3)
      if key == 'Max_Rating':
        max_r = int(rating_stat[key])
        max_list.append(max_r)
      if key == 'Average_Rating':
        ave = int(rating_stat[key])
        average_list.append(ave)
      if key == 'Year':
        year = int(rating_stat[key])
        year_list_2.append(year)
    sublist.append(year)
    sublist.append(min_r)
    sublist.append(q1)
    sublist.append(med)
    sublist.append(q3)
    sublist.append(max_r)
    sublist.append(ave)
    listlist_2.append(sublist)
  
  print(listlist_2)

  return render_template('get_trends_num_published.html', title='Trends', listlist=listlist, listlist_2=listlist_2)