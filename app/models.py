from app import db

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_manager
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    name = db.Column(db.String(64), index=True)
    emailid = db.Column(db.Integer(), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    user_to_items = db.relationship('Item', backref='id', lazy='dynamic')





class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(128))
    price = db.Column(db.Integer())
    description = db.Column(db.String(10000))
    userId = db.Column(db.Integer())
    item = db.relationship('ArtistToEvent', back_populates='artist', lazy=True)

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128))
    email_to_users = db.relationship('User', backref='emailid', lazy='dynamic')