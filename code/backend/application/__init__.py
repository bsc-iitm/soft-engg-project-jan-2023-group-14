# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This is init file for local package 'application'.

# --------------------  Imports  --------------------

from flask import Flask
from application.config import DevelopmentConfig, TestingConfig
from application.database import db
# from flask_bcrypt import Bcrypt
# import email_validator
from flask_login import LoginManager
from application.globals import API_VERSION
from application.views.auth_bp import auth_bp
from application.views.student_bp import student_bp
from application.views.support_bp import support_bp
from application.views.admin_bp import admin_bp
from application.models import Auth

# --------------------  Code  --------------------

# bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(env_type='dev'):
    app = Flask(__name__, template_folder="templates")
    if env_type == 'dev':
        app.config.from_object(DevelopmentConfig)
    if env_type == 'test':
        app.config.from_object(TestingConfig)
    db.init_app(app)
    

    # api = Api(app)
    # bcrypt.init_app(app)

    @login_manager.user_loader
    def user_loader(user_id):
        """
        Given *user_id*, return the associated User object.
        :param unicode user_id: user_id (email) user to retrieve
        """
        return Auth.query.get(user_id)

    login_manager.init_app(app) # user loader need to set

    app.register_blueprint(auth_bp, url_prefix=f'/api/{API_VERSION}/auth')
    app.register_blueprint(student_bp, url_prefix=f'/api/{API_VERSION}/student')
    app.register_blueprint(support_bp, url_prefix=f'/api/{API_VERSION}/support')
    app.register_blueprint(admin_bp, url_prefix=f'/api/{API_VERSION}/admin')

    app.app_context().push()
    db.create_all()
    db.session.commit()
    return app

# --------------------  END  --------------------
