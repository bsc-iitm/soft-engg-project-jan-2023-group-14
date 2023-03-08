# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This file contains sqlite database models (ORM).

# --------------------  Imports  --------------------

from .database import db
from flask_security import UserMixin

# --------------------  Code  --------------------


class Auth(db.Model, UserMixin):
    __tablename__ = 'auth'
    user_id = db.Column(db.String, primary_key=True)
    role = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False) 
    web_token = db.Column(db.String, unique=True, nullable=True)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    is_logged = db.Column(db.Boolean, default=False, nullable=False)
    token_created_on = db.Column(db.Integer, nullable=True)  # time is stored as a timestamp
    token_expiry_on = db.Column(db.Integer, nullable=True) 
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    profile_photo_loc = db.Column(db.String, default="", nullable=True)

    def get_id(self):
        return self.user_id
    
    def is_active(self):
        return True

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True # self.is_verified

    def is_anonymous(self):
        return False

    def __init__(self, user_id, role, email, password, first_name, last_name):
        self.user_id = user_id
        self.role = role
        self.email = email
        self.password = password  # hash password before entering
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f'Auth object for: {self.user_id} | {self.role} | {self.first_name} {self.last_name}'
        

# --------------------  END  --------------------
