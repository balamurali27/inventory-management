from flask import Blueprint, render_template

from .database import ProductMovement

bp = Blueprint('product_movements', __name__, url_prefix='/product_movements')


@bp.route('/')
def list():
    product_movements = ProductMovement.query.all()
    return render_template('product_movement_list.html',
                           product_movements=product_movements)


@bp.route('/<int:product_movement_id>/')
def detail(product_movement_id):
    product_movement = ProductMovement.query.get(product_movement_id)
    return render_template('product_movement_detail.html',
                           product_movement=product_movement)
