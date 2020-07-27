from flask import Blueprint, redirect, render_template, request, url_for

from .database import Location, Product, ProductMovement, db

bp = Blueprint('product_movements', __name__, url_prefix='/product_movements')


@bp.route('/', methods=['GET', 'POST'])
def list():

    if request.method == 'POST':
        __import__('pprint').pprint(request.form)
        from_location = Location.query.get_or_404(request.form['from_location'])
        to_location = Location.query.get_or_404(request.form['to_location'])
        product = Location.query.get_or_404(request.form['product'])
        qty = request.form['qty']
        product_movement = ProductMovement(from_location_id=from_location.id,
                                           to_location_id=to_location.id,
                                           product_id=product.id,
                                           qty=qty)
        db.session.add(product_movement)
        db.session.commit()
        return redirect(url_for('product_movements.detail',
                                product_movement_id=product_movement.id))

    product_movements = ProductMovement.query.all()
    return render_template('product_movement_list.html',
                           product_movements=product_movements,
                           locations=Location.query.all(),
                           products=Product.query.all())


@bp.route('/<int:product_movement_id>/')
def detail(product_movement_id):
    product_movement = ProductMovement.query.get_or_404(product_movement_id)
    return render_template('product_movement_detail.html',
                           product_movement=product_movement)
