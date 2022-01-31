import base64
from crypt import methods
from flask import Flask,session
from flask import render_template,request,redirect,url_for,send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import requests
import json
from config import app
import os
import base64

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
                    return redirect(url_for('home'))
                else:
                    print("Invalid Login credentials!")
                    return redirect(url_for('login'))
            else:
                return redirect(url_for('signup'))
    else:
        return redirect(url_for('home'))

@app.route('/home',methods=['GET','POST'])
def home():
    if 'user' not in session.keys() or session['user'] is None:        
        return redirect(url_for('index'))
    if request.method == 'GET':
        data = {}
        data['user'] = session['user']
        data = json.dumps(data)
        files = json.loads(requests.get('http://127.0.0.1:8000/get_user_files',data = data).json())
        print(type(files))
        return render_template('home.html',files = files,user=session['user'])
    elif request.method == 'POST':
        f = request.files['file']
        if f.filename != '':
            obj = {}
            obj['data'] = f.read()
            obj['data'] = base64.b64encode(obj['data']).decode('utf-8')
            obj['name'] = secure_filename(f.filename)
            obj['owner'] = session['user']
            obj = json.dumps(obj)
            response = requests.post('http://127.0.0.1:8000/create_file',data=obj)
        return redirect(url_for('home'))

@app.route('/delete_file/<inode>')
def delete_file(inode):
    if 'user' not in session.keys() or session['user'] is None:        
        return redirect(url_for('index'))
    data = json.dumps({'file_id':inode})
    file = json.loads(requests.get('http://127.0.0.1:8000/get_file',data = data).json())
    if file['owner'] == session['user']:
        response = json.loads(requests.get('http://127.0.0.1:8000/delete_file',data = data).text)
    return redirect(url_for('home'))



@app.route('/download_file/<inode>')
def download_file(inode):
    if 'user' not in session.keys() or session['user'] is None:        
        return redirect(url_for('index'))
    data = {}
    data['file_id'] = inode
    data = json.dumps(data)
    file = json.loads(requests.get('http://127.0.0.1:8000/get_file',data = data).json())
    os.system('mkfir files; cd files; mkdir '+file['owner']+'; cd '+file['owner']+'; mkdir '+file['inode'])
    print(file)
    f = open("files/"+file['owner']+'/'+file['inode']+'/'+file['name'],'wb')
    f.write(base64.b64decode(file['data']))
    f.close()
    return send_file("files/"+file['owner']+'/'+file['inode']+'/'+file['name'],as_attachment=True)

@app.route('/rename_file/<inode>',methods=['GET','POST'])
def rename_file(inode):
    if 'user' not in session.keys() or session['user'] is None:        
        return redirect(url_for('index'))
    if request.form.get('name') != '':
        data = json.dumps({'file_id':inode,'name':request.form.get('name')})
        file = json.loads(requests.get('http://127.0.0.1:8000/get_file',data = data).json())
        if file['owner'] == session['user']:
            response = json.loads(requests.post('http://127.0.0.1:8000/rename_file',data = data).text)
            print(response)
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
  session['user'] = None
  return redirect(url_for('index'))

if __name__ == '__main__':
  app.run(debug=True,port=8001,host='127.0.0.1')