from flask import Blueprint, render_template

from .database import ProductMovement, Product, Location, db

bp = Blueprint('balance', __name__)


@bp.route('/')
def balance():
    balances = ProductMovement.getBalances()
    rows = []
    products_n = db.session.query(Product).count()
    locations_n = db.session.query(Location).count()
    # sql index starts at 1
    for i in range(1, products_n+1):
        for j in range(1, locations_n+1):
            qty = balances.get((i, j))
            if qty is None:
                continue
            rows.append((i, j, qty))

    return render_template('balance.html', rows=rows)
