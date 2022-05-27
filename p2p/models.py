from . import db
from sqlalchemy.dialects.mysql import INTEGER
from flask_login import UserMixin

class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(INTEGER(unsigned=True), primary_key=True, unique=True)
    amount = db.Column( db.Float(150) )
    user_id = db.Column( db.Integer, nullable = False )

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    password = db.Column(db.String(150))
    name  = db.Column(db.String(150))
    phone = db.Column(db.String(150))
    
