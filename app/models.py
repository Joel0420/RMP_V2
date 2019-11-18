from datetime import datetime
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    ratings = db.relationship('Ratinf', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.relationship('Section', backref='id', lazy='dynamic')

    def __repr__(self):
        return '<Rating {}>'.format(self.id)


class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    average_rating = db.Column(db.float, index=True) #IS A FLOAT VALID HERE??!!

    def __repr__(self):
        return '<Professor {}>'.format(self.last_name)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(300), index=True)

    def __repr__(self):
        return '<Course {}>'.format(self.name)


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.relationship(db.Integer, primary_key=True)
    professor_id = db.relationship(db.Integer, primary_key=True)
    semester = db.Column(db.String(64), index=True)
    year = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Professor {}>'.format(self.id)
