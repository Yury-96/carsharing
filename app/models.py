from app import db
from datetime import datetime

class Auto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    price = db.Column(db.Float)
    description = db.Column(db.String(128))
    transmission = db.Column(db.String(20))
    img_url = db.Column(db.String(128))
    dostup = db.Column(db.String(128))

class Journal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auto_info = db.Column(db.Integer, db.ForeignKey('auto.id'))
    time_begin = db.Column(db.DateTime)
    time_end = db.Column(db.DateTime)
    cost = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    time_total = db.Column(db.Integer)
    cost_total = db.Column(db.Float)
    
    