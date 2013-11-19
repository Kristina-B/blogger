# coding: utf-8
# Удаляет и создает заново таблицы в базе данных

from sqlalchemy import create_engine

from blogger.app import app
from blogger.models import Model, Session, User

engine = create_engine(app.config['DBURI'], echo=True)
Model.metadata.drop_all(bind=engine)
Model.metadata.create_all(bind=engine)

dbs = Session()
credentials = app.config['DEFAULT_USER']
user = User(username=credentials[0], password=credentials[1])
dbs.add(user)
dbs.commit()