from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    ma.init_app(app)

    from app.login_views import login_manager
    login_manager.init_app(app)

    from app.login_views import auth
    app.register_blueprint(auth)
    from app.views import main
    app.register_blueprint(main)
    from app.ecom_views import ecom
    app.register_blueprint(ecom)
    from app.api_views import api
    app.register_blueprint(api)

    return app
