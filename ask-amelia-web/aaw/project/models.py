from flask_login import UserMixin
from . import db

# UserMixin "mixes in" flask_login attributes to the User row in the table to integrate into the class
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
