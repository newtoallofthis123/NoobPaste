from enum import unique
from paste import app, db

class Bin(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(length=80))
    hash = db.Column(db.String(length=8), unique=True, nullable=True)
    content = db.Column(db.Text())
    lang = db.Column(db.String())
    author = db.Column(db.String())
    time = db.Column(db.String())

    def __repl__(self):
        return {"title": self.title, "hash": self.hash, "content": self.content, "lang": self.lang, "author": self.author, "time":self.time}