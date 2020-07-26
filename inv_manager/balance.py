from flask import Blueprint, render_template
from sqlalchemy import func

from .database import ProductMovement, db, Location, Product

bp = Blueprint('balance', __name__, url_prefix='/')


class BalanceRow():
    """Result data structure for balance template"""

    def __init__(self, product: Product, location: Location, balance: int):
        self.product = product
        self.location = location
        self.balance = balance


@bp.route('/')
def balance():
    rows = []

    loaded = db.session.query(
        ProductMovement.product_id,
        ProductMovement.to_location_id,
        func.sum(
            ProductMovement.qty
        )
    ).filter(
        ProductMovement.to_location_id != None
    ).group_by(
        ProductMovement.to_location_id
    ).group_by(
        ProductMovement.product_id
    ).all()
    print(loaded)

    unloaded = db.session.query(
        ProductMovement.product_id,
        ProductMovement.from_location_id,
        func.sum(
            ProductMovement.qty
        )
    ).filter(
        ProductMovement.from_location_id != None
    ).group_by(
        ProductMovement.from_location_id
    ).group_by(
        ProductMovement.product_id
    ).all()
    print(unloaded)

    for i, j in zip(loaded, unloaded):
        # TODO: use joins in above query and avoid these queries <26-07-20, Balamurali M> #
        product = Product.query.get(i[0])
        location = Location.query.get(i[1])
        balance = i[2] - j[2]
        row = BalanceRow(product, location, balance)
        rows.append(row)

    return render_template('balance.html', rows=rows)
