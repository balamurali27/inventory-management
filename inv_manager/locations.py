from flask import Blueprint, render_template

from .database import Location

bp = Blueprint('locations', __name__, url_prefix='/locations')


@bp.route('/')
def list():
    locations = Location.query.all()
    return render_template('location_list.html', locations=locations)


@bp.route('/<int:location_id>/')
def detail(location_id):
    location = Location.query.get_or_404(location_id)
    return render_template('location_detail.html', location=location)
