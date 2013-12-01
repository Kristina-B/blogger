# coding: utf-8
# Объявление моделей
# Каждой модели соотвествует таблица в базе данных

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(64))

    posts = relationship('Post', backref='author')
    comments = relationship('Comment', backref='author')

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    title = db.Column(db.String(100))
    content = db.Column(db.Text)

    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    comments = relationship('Comment')

    # comment = Comment('comment body')
    # post = dbs.query(Post).get(id)
    # post.comments.add(comment)
    # dbs.commit()

    def __init__(self, title, content, author_id, created_at):
        self.title = title
        self.content = content

        self.author_id = author_id

        self.created_at = created_at


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    content = db.Column(db.Text)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime)

    def __init__(self, content, author_id, created_at):
        self.content = content
        self.author_id = author_id
        self.created_at = created_at