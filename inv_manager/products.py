from flask import Blueprint, render_template

from .database import Product

bp = Blueprint('products', __name__, url_prefix='/products')


@bp.route('/')
def list():
    products = Product.query.all()
    return render_template('product_list.html', products=products)


@bp.route('/<int:product_id>/')
def detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)
