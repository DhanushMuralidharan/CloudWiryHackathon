from config import app,db
from fastapi import Request
print("The API Server is running!")
from models import User
import datetime

print(User.query.all())

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/create_user")
async def create(info:Request):
    details = await info.json()
    if details['email'] not in [user.email for user in User.query.all()]:
        user = User(details['email'],details['name'],details['password'],datetime.date.today())
        db.session.add(user)
        db.session.commit()
        return {"message":"Account Successfully Created!","code":"success"}
    else:
        return {"message":"An account with the email ID already exists!","code":"failure"}

@app.get("/get_user_pw")
async def user_pw(info:Request):
    details = await info.json() 
    print([user.email for user in User.query.all()])
    print(details['email'])
    if details['email'] not in [user.email for user in User.query.all()]:
        return {"message":"The account does not exist!","code":"failure"}
    else:
        user = User.query.filter(User.email == details['email']).one()
        return {"password":user.password,"code":"success","message":"password has been sent!"}

   
