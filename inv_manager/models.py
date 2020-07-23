from datetime import datetime

from . import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class ProductMovement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    qty = db.Column(db.Integer, nullable=False)

    from_location_id = db.Column(db.Integer, db.ForeignKey('location.id'))

    to_location_id = db.Column(db.Integer, db.ForeignKey('location.id'))

    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
