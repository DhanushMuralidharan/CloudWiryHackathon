from config import app,db
from fastapi import Request
print("The API Server is running!")
from models import user,file
import datetime

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
    f = file(details['name'],details['owner'],details['data'])
    db.session.add(f)
    db.session.commit()
    return {"message":"File Successfully Created!","code":"success"}

