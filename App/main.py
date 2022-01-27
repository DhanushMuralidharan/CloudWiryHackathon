from flask import Flask,session
from flask import render_template,request,redirect,url_for
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import json
from config import app


@app.route('/')
def index():
    if 'user' not in session.keys() or session['user'] is None:        
        return render_template('index.html')
    else:
        return redirect(url_for('home'))

@app.route('/signup',methods = ['GET','POST'])
def signup():
    if 'user' not in session.keys() or session['user'] is None:        
        if request.method == 'GET':
            return render_template('signup.html')
        elif request.method == 'POST':
            print(request.form.get('password'),request.form.get('cpsw'))
            if request.form.get('password') == request.form.get('cpsw'):
                data = {}
                data['email'] = request.form.get('email')
                email = data['email']
                data['name'] = request.form.get('name')
                data['password'] = generate_password_hash(request.form.get('password'))
                data = json.dumps(data)
                response = json.loads(requests.post('http://127.0.0.1:8000/create_user',data = data).text)
                print(response['message'])
                if response['code'] == 'success':
                    session['user'] = email
                    return redirect(url_for('home'))
                else:
                    return redirect(url_for('signup'))
            else:
                print("Password mismatch")
                return redirect(url_for('signup'))
    else:
        return redirect(url_for('home'))

@app.route('/login',methods = ['GET','POST'])
def login():
    if 'user' not in session.keys() or session['user'] is None:        
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            data = {}
            data['email'] = request.form.get('email')
            email = data['email']
            password = request.form.get('psw')
            data = json.dumps(data)
            response = json.loads(requests.get('http://127.0.0.1:8000/get_user_pw',data = data).text)
            print(response['message'])

            if response['code'] == 'success':
                if check_password_hash(response['password'],password):
                    print("Successfully authenticated!")
                    session['user'] = email
                    return render_template('home.html')
                else:
                    print("Invalid Login credentials!")
                    return redirect(url_for('login'))
            else:
                return redirect(url_for('signup'))
    else:
        return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html')
@app.route('/logout')
def logout():
  session['user'] = None
  return redirect(url_for('index'))

if __name__ == '__main__':
  app.run(debug=True,port=8001,host='127.0.0.1')