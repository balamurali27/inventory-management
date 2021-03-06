from datetime import datetime
from typing import List, Tuple, Dict
from collections import defaultdict

import click
from flask import current_app
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()


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
    from_location = db.relationship(
        'Location', backref=db.backref('sources', lazy=True),
        foreign_keys=[from_location_id])

    to_location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    to_location = db.relationship(
        'Location', backref=db.backref('destinations', lazy=True),
        foreign_keys=[to_location_id])

    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
    product = db.relationship(
        'Product', backref=db.backref('movements', lazy=True))

    @classmethod
    def __getLoads(cls) -> List[Tuple]:
        """Get total loads in each location for each product"""
        return db.session.query(
            Product,
            Location,
            func.sum(
                cls.qty
            )
        ).join(
            Product
        ).join(
            Location,
            Location.id == cls.to_location_id
        ).filter(
            cls.to_location_id != None
        ).group_by(
            cls.to_location_id,
            cls.product_id
        ).all()

    @classmethod
    def __getUnloads(cls) -> List[Tuple]:
        """Get total unloads in each location for each product"""
        return db.session.query(
            Product,
            Location,
            func.sum(
                cls.qty
            )
        ).join(
            Product
        ).join(
            Location,
            Location.id == cls.from_location_id
        ).filter(
            cls.from_location_id != None
        ).group_by(
            cls.from_location_id,
            cls.product_id
        ).all()

    @classmethod
    def getBalances(cls) -> Dict[Product, Dict[Location, int]]:
        """Return balances of each product in each location"""

        balances = defaultdict(lambda: defaultdict(int))

        for product, location, qty in cls.__getLoads():
            balances[product][location] = qty

        for product, location, qty in cls.__getUnloads():
            balances[product][location] -= qty

        return balances


def reset_db():
    with current_app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()


@ click.command('reset-db')
@ with_appcontext
def reset_db_command():
    """Clear the existing data and create new tables."""
    reset_db()
    click.echo('Reset the database.')


def insert_dummy_data():
    with current_app.app_context():
        pro = Product(name="Kurkure")
        loc = Location(name="San Francisco")
        loc2 = Location(name="Los Angeles")
        mov = ProductMovement(product=pro, to_location=loc, qty=10)
        mov2 = ProductMovement(product=pro, to_location=loc2, qty=12)
        mov3 = ProductMovement(
            product=pro, from_location=loc2,  to_location=loc, qty=1)
        db.session.add(pro)
        db.session.add(loc)
        db.session.add(mov)
        db.session.add(mov2)
        db.session.add(mov3)
        db.session.commit()


@ click.command('insert-dummy-data')
@ with_appcontext
def insert_dummy_data_command():
    """Add dummy data to the database"""
    insert_dummy_data()
    click.echo('Added dummy data.')
