from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
db = SQLAlchemy()

# sql alchemy table class
class Todo(db.Model):
    id = sa.Column(sa.Integer,primary_key=True)
    content = sa.Column(sa.String)
    createdAt = sa.Column(sa.TIMESTAMP,default=datetime.now())
    user_id = sa.Column(sa.Integer)

class User(db.Model):
    id = sa.Column(sa.Integer,primary_key=True)
    name=sa.Column(sa.String)
    email=sa.Column(sa.String)
    password=sa.Column(sa.String)