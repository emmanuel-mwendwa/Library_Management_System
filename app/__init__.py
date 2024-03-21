from flask import Flask

from config import config

from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .services.books import book as book_blueprint
    app.register_blueprint(book_blueprint, url_prefix='/books')

    from .services.members import member as member_blueprint
    app.register_blueprint(member_blueprint, url_prefix="/members")

    from .services.transactions import transaction as transaction_blueprint
    app.register_blueprint(transaction_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api/v1")


    return app