from flask import render_template

from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': "Joel, Iyayi, Cam"}
    return render_template('index.html', title='Home', user=user)

@app.route('/about')
def about_us():
    mission_statement = {"Our mission is to create a more efficient and intuitive application of RateMyProfessor’s framework by utilizing key concepts of design and databases, specifically for Ithaca College students."
                         " RateMyProfessor uses a professor-strictly build,"
                         " whereas our website is going to take a "
                         "more intuitive approach that allows for organization by courses, and ratings of professors that pertain to specific courses they teach."}

    return render_template('about_us.html', title='About Us', paragraph=mission_statement)
