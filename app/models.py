from . import db
import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Booking(db.Model):
    room_no = db.Column(db.Integer,primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start = db.Column(db.DateTime, default = datetime.datetime.now())
    end = db.Column(db.DateTime)  