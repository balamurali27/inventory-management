from flask import Blueprint, render_template
from sqlalchemy import func

from .database import ProductMovement

bp = Blueprint('balance', __name__, url_prefix='/')


@bp.route('/')
def balance():
    balances = ProductMovement.getBalances()
    return render_template('balance.html', balances=balances)
