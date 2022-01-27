from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from config import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    email = db.Column(db.Text,nullable=False,unique=True,primary_key=True)
    name = db.Column(db.Text,nullable=False)
    password = db.Column(db.Text,nullable=False)
    date_joined = db.Column(db.Text)

    def __init__(self,email,name,password,date_joined):
        self.email = email
        self.name = name
        self.password = password
        self.date_joined = date_joined
    
