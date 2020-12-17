from app import db


class Auto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    price = db.Column(db.Integer)
    description = db.Column(db.String(128))
    transmission = db.Column(db.String(20))
    img_url = db.Column(db.String(128))

