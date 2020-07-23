from datetime import datetime

import click
from flask import current_app
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

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
        'Location', backref=db.backref('sources', lazy=True), foreign_keys=[from_location_id])

    to_location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    to_location = db.relationship(
        'Location', backref=db.backref('destinations', lazy=True), foreign_keys=[to_location_id])

    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
    product = db.relationship(
        'Product', backref=db.backref('movements', lazy=True))


def reset_db():
    with current_app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()


@click.command('reset-db')
@with_appcontext
def reset_db_command():
    """Clear the existing data and create new tables."""
    reset_db()
    click.echo('Reset the database.')


def insert_dummy_data():
    with current_app.app_context():
        pro = Product(name="Kurkure")
        loc = Location(name="san francisco")
        loc2 = Location(name="los angeles")
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


@click.command('insert-dummy-data')
@with_appcontext
def insert_dummy_data_command():
    """Add dummy data to the database"""
    insert_dummy_data()
    click.echo('Added dummy data.')
