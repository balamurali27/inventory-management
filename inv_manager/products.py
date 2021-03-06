from flask import Blueprint, redirect, render_template, request, url_for

from .database import Product, db

bp = Blueprint('products', __name__, url_prefix='/products')


@bp.route('/', methods=['GET', 'POST'])
def list():
    if request.method == 'POST':
        name = request.form['name']
        product = Product(name=name)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('products.detail', product_id=product.id))

    products = Product.query.all()
    return render_template('product_list.html', products=products)


@bp.route('/<int:product_id>/')
def detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)
