# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This file contains app configuration.

# --------------------  Imports  --------------------

from application.globals import BACKEND_ROOT_PATH
import os

# --------------------  Code  --------------------

class Config():
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///databases/supportTicketDB_Prod.sqlite3?charset=utf8'
    SECRET_KEY = 'secretKey'
    DEBUG = False


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///databases/supportTicketDB_Test.sqlite3?charset=utf8'
    SECRET_KEY = 'secretKey'
    DEBUG = True

class DevelopmentConfig(Config):
    db_path = os.path.join(BACKEND_ROOT_PATH, "databases", "supportTicketDB_Dev.sqlite3")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_path + '?charset=utf8'
    SQLALCHEMY_ECHO = True # for sqlalchemy debug queries
    SECRET_KEY = 'secretKey'
    DEBUG = True

    # SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    # SECURITY_FRESHNESS_GRACE_PERIOD = timedelta(hours=1)
    # SECURITY_PASSWORD_HASH = "bcrypt"
    # SECURITY_PASSWORD_SALT = "really super secret"
    # SECURITY_REGISTERABLE = True
    # SECURITY_CONFIRMABLE = False
    # SECURITY_SEND_REGISTER_EMAIL = False
    # SECURITY_UNAUTHORIZED_VIEW = None
    # WTF_CSRF_ENABLED = False

# --------------------  END  --------------------
