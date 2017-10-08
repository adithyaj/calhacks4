# all the imports
from flask import Flask, request, g, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from forms import LoginForm
from utils import load_keys, rand_int, hard_limit, to_str, u_rand
from geopy.geocoders import Nominatim
import os
import json
import sqlite3
from ml import ml_main

categories = ["beach", "city", "nature", "tourist"]
pq = 15
#keys = load_keys()
app = Flask(__name__) # create the application instance
app.config['SECRET_KEY'] = "calhacks" #keys['wtf_secret_key']
print(app.config['SECRET_KEY'])
app.config['DATABASE'] = os.path.join(app.root_path, 'planet.db')

geo = Nominatim()

bootstrap = Bootstrap(app)
#csrf = CsrfProtect(app)

##Database Stuff
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
        current application context.
        """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

##Database operations
def build_results(filename):
    d = {'fail':0, 'description':""}
    db = get_db()
    cursor = db.cursor()
    with open(filename) as f:
        content = f.readlines()
    for each in content:
        p = load_place(each)
        db.execute('INSERT INTO results(place, latitude, longitude, category) VALUES (?, ?, ?, ?)', (p[0], p[1], p[2], p[3]))
        cur_row = db.execute('SELECT LAST_INSERT_ROWID()').fetchone()[0]
        print("##### %s" % cur_row)
    db.commit()
    return json.dumps(d)

def load_place(place):
    s = place.split(', ')
    x = to_str(s[0], s[1], s[2])
    location = geo.geocode(x)
    if(not location):
        lat, lon = 0.0, 0.0
    else:
        lat, lon = location.latitude, location.longitude
        return (x, lat, lon, s[3])

def check_user(username, password):
    db = get_db()
    cur = db.execute('SELECT hashword FROM users WHERE username=?', (username, ))
    temp = cur.fetchone()[0]
    if(not temp or temp!=password):
        return False
    return True

##pages

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if request.method=="POST":
        session['username'] = form.username.data
        session['password'] = form.password.data
        if check_user(session['username'], session['password']):
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('index.html', form=form)

@app.route('/home')
def home():
    if(session.get('logged_in', False)):
        kv = {"user" : session['username'], "name" : session['password']}
        session['history'] = []
        session['scores'] = {x:0 for x in categories}
        session['state'] = {"lastLeft":None, "lastRight":None}
        session['count'] = 0
        return render_template('home.html', **kv)
    return redirect(url_for('index'))

@app.route('/create_user',  methods=['GET', 'POST'])
def create_user():
    form = LoginForm()
    if form.validate_on_submit():
        session['username'] = form.username.data
        session['password'] = form.password.data
        db = get_db()
        db.execute('INSERT INTO users (username, hashword) values (?, ?)', (session['username'], session['password']))
        db.commit()
        flash('User created')
        return redirect(url_for('index'))
    return render_template('create_user.html', form=form)

@app.route('/select')
def select():
    return render_template('select.html')


@app.route('/next/<direction>', methods=['GET'])
def next(direction):
    d = {}
    if(session['count'] == hard_limit):
        d['first'] = -1
        return json.dumps(d)
    print(direction)
    d['first'] = ("../static/img/x%s.jpg" % rand_int(1, 13))
    d['second'] = ("../static/img/x%s.jpg" % rand_int(1, 13))
    session['count'] += 1
    return json.dumps(d)

@app.route('/picker_start', methods=['GET'])
def picker_start():
    cat1, cat2 = u_rand(0, len(categories), 2)
    cat1 = categories[cat1]
    cat2 = categories[cat2]
    x = ("../static/img/%s%s.jpg" % (cat1, rand_int(1, pq)))
    y = ("../static/img/%s%s.jpg" % (cat2, rand_int(1, pq)))
    session['state']['lastLeft'] = cat1
    session['state']['lastRight'] = cat2
    return render_template('select.html', **{"img1":x, "img2":y})

@app.route('/picker/<direction>', methods=['GET'])
def picker(direction):
    d={}
    if(session['count'] == hard_limit):
        d['first'] = -1
        return json.dumps(d)
    session['count'] += 1
    session['history'].append(direction)
    return json.dumps(d)

@app.route('/load/<item>')
def load(item):
    return build_results('../places.txt')

@app.route('/results')
def results():
    db = get_db()
    temp = db.execute('SELECT id, place, latitude, longitude FROM results LIMIT 5')
    cur = temp.fetchall()
    ls = [tuple(x) for x in cur]
    return render_template('results.html', results_list=cur)


@app.route('/map/<id>')
def about(id):
    db = get_db()
    temp = db.execute('SELECT latitude, longitude FROM results WHERE id=?', (id,))
    cur = [tuple(x) for x in temp.fetchall()]
    cur = cur[0]
    print(cur)
    return render_template('map.html', **{"lat":cur[0], "lon":cur[1]})


if __name__ == '__main__':
    app.run(debug=True)
