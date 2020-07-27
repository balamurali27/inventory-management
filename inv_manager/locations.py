from flask import Blueprint, render_template
from flask import request, redirect, url_for

from .database import Location, db

bp = Blueprint('locations', __name__, url_prefix='/locations')


@bp.route('/', methods=['GET', 'POST'])
def list():
    if request.method == 'POST':
        name = request.form['name']
        location = Location(name=name)
        db.session.add(location)
        db.session.commit()
        return redirect(url_for('locations.detail', location_id=location.id))

    locations = Location.query.all()
    return render_template('location_list.html', locations=locations)


@bp.route('/<int:location_id>/')
def detail(location_id):
    location = Location.query.get_or_404(location_id)
    return render_template('location_detail.html', location=location)
