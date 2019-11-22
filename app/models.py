from datetime import datetime
from app import db
from flask_login import UserMixin
from app import login


class User (UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    ratings = db.relationship('Rating', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)



@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey("Section", "id"))
    section = db.relationship('Section', backref='ratings', lazy='dynamic')

    def __repr__(self):
        return '<Rating {}>'.format(self.id)


class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    average_rating = db.Column(db.Float, index=True)

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
    course_id = db.relationship(db.Integer, db.ForeignKey)  # insert not null
    professor_id = db.relationship(db.Integer, db.ForeignKey)
    semester = db.Column(db.String(64), index=True)
    year = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Professor {}>'.format(self.id)


