# coding: utf-8
# Объявление моделей
# Каждой модели соотвествует таблица в базе данных

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.ext.declarative import declarative_base

Session = scoped_session(sessionmaker())

Model = declarative_base()

#Model.query = Session.query_property()


class User(Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    password = Column(String(64))

    posts = relationship('Post', backref='author')

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Post(Model):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('user.id'))

    title = Column(String(100))
    content = Column(Text)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

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


class Comment(Model):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'))
    content = Column(Text)

    created_at = Column(DateTime)

    def __init__(self, content, created_at):
        self.content = content
        self.created_at = created_at