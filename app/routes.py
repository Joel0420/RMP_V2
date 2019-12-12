from flask import render_template, flash, redirect, url_for, abort
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.models import *
from app.forms import *
from sqlalchemy import or_
from statistics import mean

@app.route('/')
@app.route('/index')
def index():
    user = {'username': "Joel, Iyayi, Cam"}
    return render_template('index.html', title='Home', user=user)


@app.route('/about_us')
def about_us():
    mission_statement = '''Our mission is to create a more efficient and intuitive application of RateMyProfessor’s
                         framework by utilizing key concepts of design and databases, specifically for Ithaca
                         College students.'''

    return render_template('about_us.html', title='About Us', mission_statement=mission_statement)


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
            'rating': 2,
            'user_id': 1,
            'professor_id': 1

        },

        {
            'rating': 5,
            'user_id': 1,
            'professor_id': 2
        },

        {
            'rating': 7,
            'user_id': 3,
            'professor_id': 1
        },

        {
            'rating': 5,
            'user_id': 3,
            'professor_id': 2
        }
    ]

    comments = [
        {
            'comment': 'Bro you are an amazing professor what',
            'user_id': 1,
            'professor_id': 1
        },
        {
            'comment': 'Bro you are a weird professor',
            'user_id': 1,
            'professor_id': 2
        },
        {
            'comment': 'I ate in the back of class all semester',
            'user_id': 2,
            'professor_id': 1
        },
        {
            'comment': 'Weird class',
            'user_id': 2,
            'professor_id': 2
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

    professor_to_course = [
        {
            'professor_id': 1,
            'course_id': 1
        },
        {
            'professor_id': 1,
            'course_id': 2
        },
        {
            'professor_id': 2,
            'course_id': 1
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
        print('Adding to Rating {}'.format(rating))

    for comment in comments:
        c = Comment(comment=comment['comment'], user_id=comment['user_id'], professor_id=comment['professor_id'])
        db.session.add(c)
        print('Adding to Comment {}'.format(comment))

    for profToCourse in professor_to_course:
        p2c = ProfessorToCourse(professor_id=profToCourse['professor_id'], course_id=profToCourse['course_id'])
        db.session.add(p2c)
        print('Adding to ProfessorToCourse {}'.format(professor_to_course))

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
        user = User(username=form.username.data, first_name=form.first_name.data,
                    last_name=form.last_name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations you are now a registered user!")
        return redirect(url_for('login'))
    return render_template('register.html', title='register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    ratings = Rating.query.filter_by(user_id=user.id).all()

    print("Ratings:", ratings)
    if user is None:
        abort(404)
    return render_template('user.html', user=user, ratings=ratings)


@app.route('/search', methods=['GET', 'POST'])
def search_results():
    form = SearchForm()
    if form.validate_on_submit():
        search = form.searchField.data
        professors = set(Professor.query.filter(or_(Professor.first_name.like(search), Professor.last_name.like(search))).all())
        courses = set(Course.query.filter(Course.name.like(search)).all())
        for search_term in search.split():
            search_term = '%' + search_term + '%'
            professors = professors | set(Professor.query.filter(or_(Professor.first_name.like(search_term), Professor.last_name.like(search_term))).all())
            courses = courses | set(Course.query.filter(Course.name.like(search_term)).all())
            if not professors and not courses:
                flash("No Professors or Courses Match Your Search")
            else:
                return render_template('search.html', title='search results', form=form, professors=professors, courses=courses)
    return render_template('search.html', title='search results', form=form)


@app.route('/professor/<pid>')
def professor(pid):
    professor = Professor.query.filter_by(id=pid).first()
    courses = Course.query.filter(Course.professors.any(professor_id=professor.id)).all()
    ratings = Rating.query.filter(Rating.professor_id == professor.id).all()
    avg_rating = mean([rating.rating for rating in ratings])
    return render_template('professor_info.html', title="Professor Page", professor=professor, courses=courses, ratings=ratings, avg_rating=avg_rating)
