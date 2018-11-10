import os
from flask import Flask

from config import config
from flask_compress import Compress
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

basedir = os.path.abspath(os.path.dirname(__file__))

mail = Mail()
db = SQLAlchemy()
csrf = CSRFProtect()
compress = Compress()

# Set up Flask-Login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'account.login'


def create_app(config_name="dev"):
    """ Create the application """
    if not isinstance(config_name, str):
        configuration = config_name
    else:
        configuration = config[config_name]

    app = Flask(
        __name__,
        template_folder=configuration.template_folder,
        static_folder=configuration.static_folder,
        static_url_path="/statics"
    )
    app.config.from_object(configuration)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    configuration.init_app(app)

    # Set up extensions
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    #csrf.init_app(app)
    compress.init_app(app)
    #assets_env = Environment(app)

    # Register Jinja template functions
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .account import account as account_blueprint
    app.register_blueprint(account_blueprint, url_prefix='/account')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    return app