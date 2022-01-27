from fastapi import FastAPI
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = FastAPI()
db_dir = os.path.dirname(os.getcwd())+"/DB/database.sqlite3"
fapp = Flask(__name__)
fapp.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + db_dir
fapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(fapp)
