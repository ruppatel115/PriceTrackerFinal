import smtplib
import sqlite3
import flask
from flask import render_template, flash, redirect, url_for, request, jsonify
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
#import requests
#from bs4 import BeautifulSoup

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    if form.validate_on_submit():
        item = Item.query.filter_by(name=form.item_name.data).first()
        #item = Item.query.filter_by(url=form.item_url.data).first()



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
#fixed
    item = db.session.query(Item).filter(Item.name == name).first()
    highest_price = item.highest_price
    lowest_price = item.lowest_price
    current_price = item.current_price
    item_id = item.id
    name=item.name
    url=item.url
    form = SetPriceForm()
    if form.validate_on_submit():
        track_price = form.tracking_price.data
        email_temp = form.email.data
        exists = db.session.query(db.exists().where(Email.email == email_temp)).scalar()
        track = Email(email=email_temp, item_id=item_id, tracking_price=track_price)
        db.session.add(track)
        db.session.commit()

        if(track_price<current_price):

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()

            server.login('price.tracker2019@gmail.com', 'ptpassword')

            subject = 'Price dropped down for '+item.name
            body="The item you were tracking has dropped in price! Click link to purchase item at:\n "+url

            msg = "Subject: "+subject+"\n\n"+body
            server.sendmail(
                'price.tracker2019@gmail.com',

                email_temp,
                msg

            )
            print('EMAIL HAS BEEN SENT')

            server.quit()




    return render_template('item.html', form=form, name=name, url=url, highest_price=highest_price, lowest_price=lowest_price, current_price=current_price)

@app.route('/profile')
@login_required
def profile():
    u2is = current_user.items
    items = [u2i.item for u2i in u2is]
    #TODO this isn't working yet
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    # urls = [item.url for item in items]
    # imgs = []
    # for url in urls:
    #     response = requests.get(url, headers=headers)
    #     soup = BeautifulSoup(response.content, "html.parser")
    #     #itemTitle = soup.find(id="productTitle").get_text()
    #     link1 = soup.find(id="imgTagWrapperId").find('img', src=True)
    #     imglink = link1["src"].split("src=")[-1]
    #     imgs.append(imglink)

    form = WishlistForm()
    if form.validate_on_submit():
        flash('This feature is not implemented yet')
        return redirect(url_for('profile'))
    return render_template('profile.html',title='Profile', items=items, form=form)#, imgs=imgs)

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





@app.route('/data/<name>')
def data(name):


    item = db.session.query(Item).filter(Item.name == name).first()
    highest_price = Item.query.filter_by(name = name, highest_price=Item.highest_price).first().highest_price
    lowest_price = Item.query.filter_by(name= name,lowest_price=Item.lowest_price).first().lowest_price


    return jsonify({'results': sample(range(lowest_price, highest_price),12)})

