"""These are database models"""

from flask_sqlalchemy import SQLAlchemy

# database import, global scope
DB = SQLAlchemy()

class User(DB.Model):
    """Twitter users to analyze"""
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)

class Tweet(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    text = DB.Column(DB.Unicode(280))
