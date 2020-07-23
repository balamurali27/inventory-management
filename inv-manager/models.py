from datetime import datetime

from . import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class ProductMovement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    from_location = db.relationship(
        'Location', backref=db.backref('movementStarts', lazy=True))
    to_location = db.relationship(
        'Location', backref=db.backref('movementEnds', lazy=True))
    product = db.relationship(
        'Product', backref=db.backref('movements', lazy=True), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
