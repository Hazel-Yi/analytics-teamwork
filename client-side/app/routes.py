from flask import Flask, render_template, request
from app import app


@app.route('/')
@app.route('/get_boardgame')
def get_boardgame():
  '''get data from the file'''
  return render_template('get_boardgame.html', title='Get Boardgames')

@app.route('/get_boardgame_id', methods=['GET', 'POST'])
def get_boardgame_id():
  if request.method == 'POST':
    search_id = request.form['search']
    print("searched for a game with id " + search_id) 
    '''get data from the file'''
    name = "abc"
    image = "abc"
    published_by = "abc"
    categories = "abc"
    description = "abc"
    expansions = "abc"
    return render_template('get_boardgame_id_2.html', title='Get Boardgame ID', name=name, image=image, published_by=published_by, categories=categories, description=description, expansions=expansions)
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
