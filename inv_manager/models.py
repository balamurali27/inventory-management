from datetime import datetime

from . import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)


class ProductMovement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    qty = db.Column(db.Integer, nullable=False)

    from_location_id = db.Column(db.Integer, db.ForeignKey('location.id'))

    to_location_id = db.Column(db.Integer, db.ForeignKey('location.id'))

    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
