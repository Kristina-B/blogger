#!/usr/bin/env python
# coding: utf-8
# Удаляет и создает заново таблицы в базе данных


from blogger.app import app
from blogger.models import db, User

with app.test_request_context():
    db.drop_all()
    db.create_all()

    credentials = app.config['DEFAULT_USER']
    user = User(username=credentials[0], password=credentials[1])
    db.session.add(user)
    db.session.commit()