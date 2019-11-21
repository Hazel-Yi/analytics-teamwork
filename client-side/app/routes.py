from flask import Flask, render_template, request
import requests
from app import app
import json

@app.route('/')
@app.route('/get_boardgame')
def get_boardgame():
  r = requests.get("http://127.0.0.1:8000/details", params={'order': 'Game_ID', 'ascending':True})
  games = r.json()

  h = games[1]
  print(h)

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

  print(listlist[0])

  return render_template('get_boardgame.html', title='Get Boardgames', listlist=listlist, game_id_list=game_id_list[0:10], name_list=name_list[0:10], year_list=year_list[0:10])
    

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
    print(name)
    return render_template('get_boardgame_id_2.html', title='Get Boardgame ID', name=name, published_by=published_by, categories=categories, description=description, expansions=expansions)
  else:
    return render_template('get_boardgame_id.html', title='Get Boardgame ID')

@app.route('/get_rec', methods=['GET', 'POST'])
def get_rec():
  '''get 30 recommended games provided by the ML model'''
  if request.method == 'POST':
    search_id = request.form['search']
    num_rec = request.form['num_rec']
    print("searched for a game with id " + search_id + " and " + num_rec + " number of rec")
    return render_template('get_rec_2.html', title='Get Recommendation', num_rec=num_rec) 
  else:
    return render_template('get_rec.html', title='Get Recommendation')

@app.route('/post_boardgame', methods=['GET', 'POST'])
def post_boardgame():
  if request.method == 'POST':
    game_id = request.form['id']
    name = request.form['name']
    published_by = request.form['published_by']
    categories = request.form['categories']
    min_players = request.form['min_players']
    max_players = request.form['max_players']
    min_age = request.form['min_age']
    min_playtime = request.form['min_playtime']
    description = request.form['description']
    expansions = request.form['expansions']
    mechanics = request.form['mechanics']
    thumbnail = request.form['thumbnail']
    year = request.form['year']
    print(name)
    game = {
      'Game_ID': game_id,
      'Name': name,
      'Publisher': published_by,
      'Category': categories,
      'Min_players': min_players,
      'Max_players': max_players,
      'Min_age': min_age,
      'Min_playtime': min_playtime,
      'Description': description,
      'Expansion': expansions,
      'Mechanic': mechanics,
      'Thumbnail': thumbnail,
      'Year_Published': year
    }
    print(game)

    r = requests.post("http://127.0.0.1:8000/details", json=game)

    print("Status Code:" + str(r.status_code))
    resp = r.json()

    print(resp['message'])

  return render_template('post_boardgame.html', title='Post Boardgame')

@app.route('/put_boardgame')
def put_boardgame():
  return render_template('put_boardgame.html', title='Put Boardgame')