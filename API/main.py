from config import app,db
from fastapi import Request
print("The API Server is running!")
from models import user,file
import datetime
import json


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
    f = file(details['name'],details['owner'],bytes(details['data'],'utf-8'))
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
        db.session.commit()
        return {"message":"file has been renamed successfully!","code":"success"}

@app.post("/delete_file")
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
        return json.dumps({'name':f.name,'inode':f.inode,'data':f.data.decode(),'date-created':f.date_created,'date-modified':f.date_modified,'owner':f.owner})