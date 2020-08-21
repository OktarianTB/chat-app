from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(25), db.ForeignKey("users.username"), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(10), nullable=False)
