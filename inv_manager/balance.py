from flask import Blueprint, render_template
from sqlalchemy import func

from .database import ProductMovement, db, Location, Product

bp = Blueprint('balance', __name__, url_prefix='/')


@bp.route('/')
def balance():
    locations = Location.query.all()
    products = Product.query.all()
    for product in products:
        for location in locations:
            loaded = db.session.query(
                func.sum(
                    ProductMovement.qty
                )
            ).select_from(
                ProductMovement
            ).filter(
                ProductMovement.to_location == location,
                ProductMovement.product == product
            ).first()[0]
            # TODO: use group by for location instead of iterator <26-07-20, Balamurali M> #
            # TODO: try group by for product too if location group by was possible <26-07-20, Balamurali M> #

            unloaded = db.session.query(
                func.sum(
                    ProductMovement.qty
                )
            ).select_from(
                ProductMovement
            ).filter(
                ProductMovement.from_location == location,
                ProductMovement.product == product
            ).first()[0]

            unloaded = 0 if unloaded is None else unloaded
            loaded = 0 if loaded is None else loaded
            balance = loaded - unloaded
            print("balance ", product.name, location.name, balance)

    return render_template('base.html')
