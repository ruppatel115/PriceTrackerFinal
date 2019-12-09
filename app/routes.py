import sqlite3

import flask
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db, models
from app.forms import *
from flask_login import LoginManager
from app.models import *
from datetime import datetime
from random import sample
from flask_wtf import Form
from wtforms import Form, StringField, TextAreaField, SubmitField, PasswordField, BooleanField, DateField, SelectField, SelectMultipleField, IntegerField

#
#
# @app.route('/test')
# def search():
#    term = flask.request.args.get('query')
#    possibilities = [i for [i] in sqlite3.connect('app.db').cursor().execute("SELECT * FROM videos WHERE title LIKE %s", ("%" + user_input + "%")]
#    return flask.jsonify({'html':'<p>No results found</p>' if not possibilities else '<ul>\n{}</ul>'.format('\n'.join('<li>{}</li>'.format(i) for i in possibilities))})


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    #if request.method=='POST':
    if form.validate_on_submit():
        item = Item.query.filter_by(name=form.item_name.data).first()
        if item is None:
            flash('Invalid item')
            return redirect(url_for('home'))
        return redirect(url_for('item', name=item.name))
        #return render_template('home.html', title='Home', form=form)

    return render_template('home.html', title='Home', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)




@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/reset')
def reset_db():
    flash("Resetting database: deleting old data")
    # clear all data from all tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())

    return redirect(url_for('home'))

@app.route('/item/<name>', methods=['GET', 'POST'])
def item(name):
    #url = Item.query.filter_by(url=Item.url)
    form = SetPriceForm()
    return render_template('item.html', form=form, name=name) #TODO item parameter

@app.route('/profile')
@login_required
def profile():
    currentuser = User.query.filter_by(username={{current_user.username}}).first()
    useritems = Item.query.filter_by(userId=currentuser.id).all()

    return render_template('profile.html',title='Profile', items=useritems)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_profile.html', title='Edit Profile',form=form)


@app.route('/data')
def data():
    my_items=item.query.all()
    return render_template('data.html', my_items=my_items)


