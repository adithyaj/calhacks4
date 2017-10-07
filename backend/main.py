# all the imports
from flask import Flask, request, render_template
from utils import load_keys

keys = load_keys()
app = Flask(__name__) # create the application instance



@app.route('/')
def home():
    kv = {"user" : "Shivam", "name" : "Parikh"}
    return render_template('index.html', **kv)

@app.route('/user')
def ua():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s</p>' % user_agent


if __name__ == '__main__':
    app.run(debug=True)
