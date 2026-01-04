from extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20), default="uye")

    # bookmarks relationship
    bookmarks = db.relationship('Bookmark', back_populates='user', cascade='all, delete-orphan')

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # simple category field (string)
    category = db.Column(db.String(100), nullable=True)

    # optional image filename
    image = db.Column(db.String(200), nullable=True)

    # bookmarks relationship
    bookmarks = db.relationship('Bookmark', back_populates='news', cascade='all, delete-orphan')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    news_id = db.Column(db.Integer, db.ForeignKey("news.id"))

    # parent comment for replies
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    parent = db.relationship('Comment', remote_side=[id], backref=db.backref('replies', cascade='all, delete-orphan'))

    # relationship to author user
    user = db.relationship('User', backref='comments')

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='bookmarks')
    news = db.relationship('News', back_populates='bookmarks')
