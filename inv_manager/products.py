from flask import Blueprint, render_template

from .models import Product

bp = Blueprint('products', __name__, url_prefix='/products')


@bp.route('/')
def list():
    products = Product.query.all()
    return render_template('product_list.html', products=products)


@bp.route('/<int:product_id>/')
def detail(product_id):
    product = Product.query.filter_by(id=product_id).first()
    return render_template('product_detail.html', product=product)
