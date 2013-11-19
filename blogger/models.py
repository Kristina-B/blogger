# coding: utf-8
# Объявление моделей
# Каждой модели соотвествует таблица в базе данных

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.ext.declarative import declarative_base

from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required, EqualTo

Session = scoped_session(sessionmaker())

Model = declarative_base()


class User(Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    password = Column(String(64))

    posts = relationship('Post', backref='author')


class RegistrationForm(Form):
    __tablename__ = 'registration_form'

    name = TextField('Username', [Required()])
    password = PasswordField('Password', [Required()])
    confirm = PasswordField('Repeat Password', [Required(),EqualTo('password', message='Passwords must match')])


class Post(Model):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('user.id'))

    title = Column(String(100))
    content = Column(Text)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    comments = relationship('Comment')


class Comment(Model):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'))
    content = Column(Text)

    created_at = Column(DateTime)