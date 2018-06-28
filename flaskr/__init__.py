import os

from flask import Flask
from . import routes


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    UPLOAD_FOLDER = './uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    @app.route("/")
    def index():
        return "Welcome to the index of the speech to text API"
    app.register_blueprint(routes.bp)
    return app
