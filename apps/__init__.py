# import mysql.connector
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jsglue import JSGlue
from apps.config import Config
from apps.celery import FlaskCelery


celery = FlaskCelery()
db = SQLAlchemy()
jsglue = JSGlue()
login_manager = LoginManager()
login_manager.login_view = 'accounts.login'
login_manager.login_message_category = 'danger'
login_manager.login_message = 'Anda belum login!'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    celery.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    jsglue.init_app(app)

    from apps.controllers.accounts.routes import accounts
    from apps.controllers.dashboards.routes import dashboards
    from apps.controllers.datasets.routes import datasets
    from apps.controllers.feature.routes import feature
    from apps.controllers.classification.routes import classification
    from apps.controllers.main.routes import main
    from apps.controllers.errors.handlers import errors

    app.register_blueprint(accounts)
    app.register_blueprint(dashboards)
    app.register_blueprint(datasets)
    app.register_blueprint(feature)
    app.register_blueprint(classification)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
