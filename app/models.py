from app import db

from flask_login import UserMixin


class User(UserMixin,db.Model):
  id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
  email = db.Column(db.String(100), unique=True)
  password = db.Column(db.String(100))
  name = db.Column(db.String(1000))

  def __repr__(self):
    return f"{self.email} - {self.id}"

class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(550),nullable=False)
  status = db.Column(db.String(20), default="Pending")

  def __repr__(self):
    return f"{self.title} - {self.id}"