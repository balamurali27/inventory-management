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

    to_location_id = db.Column(db.Integer, db.ForeignKey('location.id'))

    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)


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
        db.session.add(pro)
        db.session.add(loc)
        db.session.commit()


@click.command('insert-dummy-data')
@with_appcontext
def insert_dummy_data_command():
    """Add dummy data to the database"""
    insert_dummy_data()
    click.echo('Added dummy data.')
