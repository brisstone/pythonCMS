from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    email = email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128), nullable = False)
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    adm = db.Column(db.Boolean(), default= 0)