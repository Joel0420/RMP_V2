from datetime import datetime
from app import db
from flask_login import UserMixin
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
import flask_whooshalchemy
from whoosh.analysis import StemmingAnalyzer


# Each User can have multiple comments/ratings, but each rating/comment can only have one User
# Each Professor can receive multiple comments/ratings, but each rating/comment can only have one Professor


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    ratings = db.relationship('Rating', backref='user', lazy='dynamic')
    courses = db.relationship('UserToCourse', backref='user', lazy='dynamic')

    # ratings creates an SQLAlchemy Object that allows for queries to be made
    # backref='user' allows for us to type Rating.user.first_name, and access those values
    # list is accessed with User.ratings.all()

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Professor(db.Model):
    __tablename__ = 'professor'
    __searchable__ = ['first_name', 'last_name']  # these fields will be indexed by whoosh
    __analyzer__ = StemmingAnalyzer()

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    ratings = db.relationship('Rating', backref='professor', lazy='dynamic')
    courses = db.relationship('ProfessorToCourse', backref='professor', lazy='dynamic')

    def __repr__(self):
        return '<Professor {}>'.format(self.last_name)


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'))

    def __repr__(self):
        return '<Rating {}>'.format(self.id)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(400), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'))

    def __repr__(self):
        return '<Comment {}>'.format(self.id)


# Each User can have multiple courses, each course can have multiple users
# Each Professor can have multiple courses, each course can have multiple professors
# ProfessorToCourse class required to mitigate that relationship


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(300), index=True)
    professors = db.relationship('ProfessorToCourse', backref='course', lazy='dynamic')

    def __repr__(self):
        return '<Course {}>'.format(self.name)


class ProfessorToCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    def __repr__(self):
        return '<ProfessorToCourse {}>'.format(self.id)


class UserToCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    def __repr__(self):
        return '<UserToCourse {}>'.format(self.id)
