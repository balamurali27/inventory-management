from flask import Blueprint, render_template

from .database import ProductMovement, Product, Location, db

bp = Blueprint('balance', __name__)


@bp.route('/')
def balance():
    balances = ProductMovement.getBalances()
    rows = []
    products = Product.query.all()
    locations = Location.query.all()
    # sql index starts at 1
    for product in products:
        for location in locations:
            qty = balances.get((product, location))
            if qty is None:
                continue
            rows.append((product, location, qty))

    return render_template('balance.html', rows=rows)
