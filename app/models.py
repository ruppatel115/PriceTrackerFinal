from wtforms import ValidationError

from app import db, login
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_manager
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    items = db.relationship('UserToItem', back_populates='user', lazy='dynamic')


    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(128))
    current_price = db.Column(db.Integer())
    highest_price = db.Column(db.Integer())
    lowest_price = db.Column(db.Integer())
    description = db.Column(db.String(10000))
    #user_to_items = db.relationship('User', backref='item', lazy='dynamic')
    users = db.relationship('UserToItem', back_populates='item', lazy=True)
    item_to_time = db.relationship('ItemToTime', backref='item', lazy='dynamic')
    item_to_email = db.relationship('Email', backref='item', lazy='dynamic')
    
class ItemToTime(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  itemid = db.Column(db.Integer(), db.ForeignKey('item.id'))
  datetime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  price = db.Column(db.Integer())



class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128))
    itemid = db.Column(db.Integer(), db.ForeignKey('item.id'))
    #email_to_users = db.relationship('User', backref='user', lazy='dynamic')

class UserToItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(),db.ForeignKey('user.id'))
    item_id = db.Column(db.Integer(), db.ForeignKey('item.id'))
    user = db.relationship('User', backref="item", lazy=True)
    item = db.relationship('Item', backref="user", lazy=True)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))