from flask import Blueprint, render_template

from .database import ProductMovement

bp = Blueprint('balance', __name__)


@bp.route('/')
def balance():
    balances = ProductMovement.getBalances()
    rows = []
    for product, locations in balances.items():
        for location, qty in locations.items():
            rows.append((product, location, qty))

    return render_template('balance.html', rows=rows)
