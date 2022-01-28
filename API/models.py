import datetime
from uuid import uuid1
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from config import db
from werkzeug.security import generate_password_hash, check_password_hash

class user(db.Model):
    email = db.Column(db.Text,nullable=False,unique=True,primary_key=True)
    name = db.Column(db.Text,nullable=False)
    password = db.Column(db.Text,nullable=False)
    date_joined = db.Column(db.Text)
    files = relationship("file",back_populates = "FileOwner")
    def __init__(self,email,name,password,date_joined):
        self.email = email
        self.name = name
        self.password = password
        self.date_joined = date_joined


class file(db.Model):
    inode = db.Column(db.Text,nullable=False,unique=True,primary_key=True)
    name = db.Column(db.Text,nullable=False)
    date_created = db.Column(db.Text)
    date_modified = db.Column(db.Text)
    owner = db.Column(db.Integer,ForeignKey('user.email'),nullable=False)
    data = db.Column(db.LargeBinary)
    FileOwner = relationship('user',back_populates = "files")
    def __init__(self,name,owner,data):
        self.name = name
        self.owner = owner
        self.inode = str(uuid1())
        self.data = data
        self.date_created = datetime.date.today()
        self.date_modified = datetime.date.today()



