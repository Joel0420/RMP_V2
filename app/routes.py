from flask import render_template, flash

from app import app, db
from app.models import *


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

    c1 = Course(name="COMP 171", description="Intro To Computer Science learning Python through simple IDE's" )
    db.session.add(c1)
    db.commit()

    c1 = Course(name="COMP 172", description="Intro To Computer Science 2, Learning Java and Object Oriented Programming")
    db.session.add(c1)
    db.commit()





