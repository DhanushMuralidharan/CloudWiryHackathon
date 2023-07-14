from urllib import request
from config import app,db
from fastapi import Request
from models import user,file
import datetime
import json
import base64
# from cryptography.fernet import Fernet
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# password='secretkeypassword'

# def generate_key(password, salt):
#     kdf = PBKDF2HMAC(
#         algorithm=hashes.SHA256(),
#         length=32,
#         salt=salt,
#         iterations=100000,
#     )
#     return kdf.derive(password)


# def encrypt(message, password):
#     salt = b'salt_'
#     key = generate_key(password.encode(), salt)
#     cipher_suite = Fernet(key)
#     cipher_text = cipher_suite.encrypt(message.encode())
#     return cipher_text


# def decrypt(cipher_text, password):
#     salt = b'salt_'
#     key = generate_key(password.encode(), salt)
#     cipher_suite = Fernet(key)
#     plain_text = cipher_suite.decrypt(cipher_text)
#     return plain_text.decode()



print("The API Server is running!")


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/create_user")
async def create(info:Request):
    details = await info.json()
    if details['email'] not in [u.email for u in user.query.all()]:
        u = user(details['email'],details['name'],details['password'],datetime.date.today())
        db.session.add(u)
        db.session.commit()
        return {"message":"Account Successfully Created!","code":"success"}
    else:
        return {"message":"An account with the email ID already exists!","code":"failure"}

@app.get("/get_user_pw")
async def user_pw(info:Request):
    details = await info.json() 
    if details['email'] not in [u.email for u in user.query.all()]:
        return {"message":"The account does not exist!","code":"failure"}
    else:
        u = user.query.filter(user.email == details['email']).one()
        return {"password":u.password,"code":"success","message":"password has been sent!"}

@app.post("/create_file")
async def create_file(info:Request):
    details = await info.json()
    f = file(details['name'],details['owner'],base64.b64decode(details['data']))
    db.session.add(f)
    db.session.commit()
    return {"message":"File Successfully Created!","code":"success"}

@app.post("/rename_file")
async def rename_file(info:Request):
    details = await info.json()
    file_id = details['file_id']
    if file_id not in [f.inode for f in file.query.all()]:
        return {"message":"The file does not exist.","code":"failure"}
    else:
        f = file.query.filter(file.inode == file_id).one()
        f.name = details['name']
        f.date_modified = datetime.date.today()
        db.session.commit()
        return {"message":"file has been renamed successfully!","code":"success"}

@app.get("/delete_file")
async def delete_file(info:Request):
    details = await info.json()
    file_id = details['file_id']
    if file_id not in [f.inode for f in file.query.all()]:
        return {"message":"The file does not exist.","code":"failure"}
    else:
        f = file.query.filter(file.inode == file_id).one()
        db.session.delete(f)
        db.session.commit()
        return {"message":"file has been deleted successfully!","code":"success"}

@app.get("/get_file")
async def get_file(info:Request):
    details = await info.json()
    file_id = details['file_id']
    if file_id not in [f.inode for f in file.query.all()]:
        return {"message":"The file does not exist.","code":"failure"}
    else:
        f = file.query.filter(file.inode == file_id).one()
        data = base64.b64encode(f.data).decode('utf-8')
        return json.dumps({'name':f.name,'inode':f.inode,'data': data,'date-created':f.date_created,'date-modified':f.date_modified,'owner':f.owner})

@app.get("/get_user_files")
async def get_user_files(info:Request):
    details = await info.json()
    u_email = details['user']
    if u_email not in [u.email for u in user.query.all()]:
        return {"message":"The user does not exist.","code":"failure"}
    else:
        f = file.query.filter(file.owner == u_email)
        data = []
        for FILE in f:
            d = base64.b64encode(FILE.data).decode('utf-8')
            temp = {'name':FILE.name,'inode':FILE.inode,'data': d,'date-created':FILE.date_created,'date-modified':FILE.date_modified,'owner':FILE.owner}
            data.append(temp)
        return json.dumps(data)
