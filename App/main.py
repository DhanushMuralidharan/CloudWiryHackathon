from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return "Sign Up Page!"

if __name__ == '__main__':
  app.run(debug=True,port=8000,host='127.0.0.1')