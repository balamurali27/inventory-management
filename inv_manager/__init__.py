import os

from flask import Flask

from .database import db, reset_db_command, insert_dummy_data_command


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///db.sqlite3',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    db.init_app(app)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.cli.add_command(reset_db_command)
    app.cli.add_command(insert_dummy_data_command)

    from . import products, locations
    app.register_blueprint(products.bp)
    app.register_blueprint(locations.bp)

    return app
