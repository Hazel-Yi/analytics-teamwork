from flask import Flask, render_template, request
import requests
from app import app
import json

@app.route('/')
@app.route('/get_boardgame')
def get_boardgame():
  r = requests.get("http://127.0.0.1:8000/games", params={'order': 'Name', 'ascending':True})
  games = r.json()
  game = games[1]
  for key in game.keys():
    if key == 'ID':
      game_id = str(game[key])
    if key == 'Name':
      name = str(game[key])
    if key == 'Year Published':
      year = str(game[key])
  print(game_id + name + year)
  return render_template('get_boardgame.html', title='Get Boardgames', game_id=game_id, name=name, year=year)
    

@app.route('/get_boardgame_id', methods=['GET', 'POST'])
def get_boardgame_id():
  if request.method == 'POST':
    search_id = request.form['search']
    print("searched for a game with id " + search_id) 
    r = requests.get("http://127.0.0.1:8000/games/" + str(search_id))
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
    name = request.form['name']
    published_by = request.form['published_by']
    image = request.form['image']
    categories = request.form['categories']
    description = request.form['description']
    expansions = request.form['expansions']
    print(name)
    '''submit a new review for a game'''
  return render_template('post_boardgame.html', title='Post Boardgame')

@app.route('/put_boardgame')
def put_boardgame():
  return render_template('put_boardgame.html', title='Put Boardgame')