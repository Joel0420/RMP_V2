from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
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

    users = [
        {
            'username': 'jay',
            'first_name': 'Joel',
            'last_name': 'Jerez',
            'email': 'jrez@gmail.com',
            'password_hash': 'TopSecret'
        },

        {
            'username': 'cam1',
            'first_name': 'Cam',
            'last_name': 'Reddish',
            'email': 'cred@gmail.com',
            'password_hash': 'NBAPlayer'
        }
    ]

    ratings = [
        {
            'rating': '2',
            'user_id': '1',
            'professor_id': '1'

        },

        {
            'rating': '5',
            'user_id': '1',
            'professor_id': '2'
        },

        {
            'rating': '7',
            'user_id': '2',
            'professor_id': '1'
        },

        {
            'rating': '5',
            'user_id': '2',
            'professor_id': '2'
        }
    ]

    comments = [
        {
            'comment': 'Bro you are an amazing professor what',
            'user_id':'1',
            'professor_id':'1'
        },
        {
            'comment': 'Bro you are a weird professor',
            'user_id': '1',
            'professor_id': '2'
        },
        {
            'comment': 'I ate in the back of class all semester',
            'user_id': '2',
            'professor_id': '1'
        },
        {
            'comment': 'Weird class',
            'user_id': '2',
            'professor_id': '2'
        },
    ]

    professors = [
        {
            'first_name': 'Doug',
            'last_name': 'Turnbull'
        },
        {
            'first_name': 'Ali',
            'last_name': 'Erkan'
        }
    ]

    courses = [
        {
            'name': 'COMP 171',
            'description': 'Intro to computer science learning python through simple IDE work',
        },
        {
            'name': 'COMP 172',
            'description': 'Intro to computer science 2, learning java and OOP'
        }
    ]

    for user in users:
        u = User(username=user['username'], first_name=user['first_name'], last_name=user['last_name'],
                 email=user['email'], password_hash=user['password_hash'])
        db.session.add(u)
        print('Adding to User {}'.format(user))

    for professor in professors:
        p = Professor(first_name=professor['first_name'], last_name=professor['last_name'])
        db.session.add(p)
        print('Adding to Professor {}'.format(professor))

    for course in courses:
        c = Course(name=course['name'], description=course['description'])
        db.session.add(c)
        print('Adding to Course {}'.format(course))

    for rating in ratings:
        r = Rating(rating=rating['rating'], user_id=rating['user_id'], professor_id=rating['professor_id'])
        db.session.add(r)
        print('Adding to Rating {}'.format(course))

    for comment in comments:
        c = Comment(comment=comment['comment'], user_id=comment['user_id'], professor_id=comment['professor_id'])
        db.session.add(c)
        print('Adding to Comment {}'.format(course))

    db.session.commit()
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


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
