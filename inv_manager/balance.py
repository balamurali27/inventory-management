from flask import Blueprint, render_template

from .database import ProductMovement

bp = Blueprint('balance', __name__)


@bp.route('/')
def balance():
    balances = ProductMovement.getBalances()
    rows = []
    for row in enumerate(balances, start=1):
        for col in enumerate(row[1], start=1):
            location = col[0]
            product = row[0]
            qty = col[1]
            rows.append((product, location, qty))

    return render_template('balance.html', rows=rows)
