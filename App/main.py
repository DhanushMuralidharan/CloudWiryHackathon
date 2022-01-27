from flask import Flask
from flask import render_template,request
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/signup',methods = ['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        print(request.form.get('password'),request.form.get('cpsw'))
        if request.form.get('password') == request.form.get('cpsw'):
            data = {}
            data['email'] = request.form.get('email')
            data['name'] = request.form.get('name')
            data['password'] = generate_password_hash(request.form.get('password'))
            data = json.dumps(data)
            response = json.loads(requests.post('http://127.0.0.1:8000/create_user',data = data).text)
            if response['code'] == 'success':
                print(response['message'])
                return render_template('home.html')
            else:
                print(response['message'])
                return render_template('signup.html')
        else:
            print("Password mismatch")
            return render_template('signup.html')

@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = {}
        data['email'] = request.form.get('email')
        password = request.form.get('psw')
        data = json.dumps(data)
        response = json.loads(requests.get('http://127.0.0.1:8000/get_user_pw',data = data).text)
        print(response)

        if response['status'] == 'success':
            if check_password_hash(response['password'],password):
                print("Successfully authenticated!")
                return render_template('home.html')
            else:
                print("Invalid Login credentials!")
        else:
            return render_template('signup.html')


if __name__ == '__main__':
  app.run(debug=True,port=8001,host='127.0.0.1')