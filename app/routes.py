from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user
from app import app, db
from app.models import *
from app.forms import *


@app.route('/')
@app.route('/index')
def index():
    user = {'username': "Joel, Iyayi, Cam"}
    return render_template('index.html', title='Home', user=user)


@app.route('/about')
def about_us():
    mission_statement = {"Our mission is to create a more efficient and intuitive application of RateMyProfessor’s "
                         "framework by utilizing key concepts of design and databases, specifically for Ithaca "
                         "College students. "
                         " RateMyProfessor uses a professor-strictly build,"
                         " whereas our website is going to take a "
                         "more intuitive approach that allows for organization by courses, and ratings of professors "
                         "that pertain to specific courses they teach."}

    return render_template('about_us.html', title='About Us', paragraph=mission_statement)


@app.route('/reset_db')
def reset_db():
    flash("Resetting database: deleting old data and repopulating with dummy data")
    # clear all data from all tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()

    c1 = Course(name="COMP 171", description="Intro To Computer Science learning Python through simple IDE's")
    db.session.add(c1)
    db.commit()

    c1 = Course(name="COMP 172",
                description="Intro To Computer Science 2, Learning Java and Object Oriented Programming")
    db.session.add(c1)
    db.commit()

    p1 = Professor(first_name="Doug", last_name="Turnbull", average_rating=4)
    db.session.add(p1)
    db.commit()

    p2 = Professor(first_name="Ali", last_name="Erkan", average_rating=4)
    db.session.add(p2)
    db.commit()

    u1 = User(username="jay", first_name="Joel", last_name="Jerez", email="jrez@gmail.com")
    db.session.add(u1)
    db.commit()

    u2 = User(username="cam_1", first_name="Cam", last_name="Reddish", email="cred@gmail.com")
    db.session.add(u2)
    db.commit()

    return render_template('index.html', title='Home')


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/index')
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations you are now a registered user!")
        return redirect('/login')
    return render_template('register.html', title='register', form=form)
