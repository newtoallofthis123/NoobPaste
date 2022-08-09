from enum import unique
from paste import app, db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Bin(db.Model):
    __tablename__ = 'paste'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(length=80))
    hash = db.Column(db.String(length=8), unique=True, nullable=True)
    content = db.Column(db.Text())
    lang = db.Column(db.String())
    password = db.Column(db.String())
    author = db.Column(db.String())
    time = db.Column(db.String())

    def __init__(self, title, hash, content, lang, author, time, password):
        self.title = title
        self.hash = hash
        self.content = content
        self.lang = lang
        self.author = author
        self.time = time
        self.password = password

    def __repr__(self):
        return '<id {}>'.format(self.id)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=40), nullable=False)
    email = db.Column(db.String(length=40))
    password_hashed = db.Column(db.String(length=240), nullable=False)
    time = db.Column(db.String())

    def __init__(self, username, email, password_hashed, time):
        self.username = username
        self.password_hashed = password_hashed
        self.email = email
        self.time = time

    def __repr__(self):
        return '<id {}>'.format(self.id)

class News_letter(db.Model):
    __tablename__ = 'news_letter'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(length=40))
    time = db.Column(db.String())

    def __init__(self, email, time):
        self.email = email
        self.time = time

    def __repr__(self):
        return '<id {}>'.format(self.id)