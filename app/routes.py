from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import *
from flask_login import LoginManager
from app.models import *
from datetime import datetime



@app.route('/')
@app.route('/home')
def home():
    # user = {'username': 'Miguel'}
    # posts = [
    #     {
    #         'author': {'username': 'John'},
    #         'body': 'Beautiful day in Portland!'
    #     },
    #     {
    #         'author': {'username': 'Susan'},
    #         'body': 'The Avengers movie was so cool!'
    #     }
    # ]
    return render_template('home.html', title='Home')


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

@app.route('/item', methods=['GET', 'POST'])
def item():
    #addmore database stuff for page
    if request.method == 'POST':
        url = request.form['url']
        legend = 'Monthly Data'
        labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
        values = [10, 9, 8, 7, 6, 4, 7, 8]
        return render_template('item.html', url=url, values=values, labels=labels, legend=legend)
    return render_template('home.html')

@app.route('/profile')
@login_required
def profile():
    # currentuser = User.query.filter_by(username={{current_user.name}}).first()
    # useritems = Item.query.filter_by(userId=currentuser.id).all()

    return render_template('profile.html',title='Profile')#,items=useritems)