# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This file contains auth related methods.

# --------------------  Imports  --------------------

# from flask import Blueprint
# from flask_restful import Api, Resource
# from application.logger import logger
import re
from flask import current_app as app
from datetime import datetime, timedelta
import time
import jwt
from application.globals import TOKEN_VALIDITY
from application.database import db
from application.models import Auth

# --------------------  Code  --------------------


class AuthUtils:
    def __init__(self, user_id=None):
        self.user_id = user_id
        self.user = None

    def __repr__(self) -> str:
        return f"Auth_Utils object for user: {self.user_id}"

    def is_blank(self, string):
        # for "", "  ", None : True else False
        return not (bool(string and not string.isspace()))

    def is_email_valid(self, email):
        regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        return re.search(regex, email)

    def is_password_valid(self, password):
        valid = list("abcdefghijklmnopqrstuvwxyz0123456789")
        if (len(password) >= 4) and (len(password) <= 10):
            for i in password:
                if i not in valid:
                    return False
            return True
        else:
            return False

    def verify_user_details(self, details: dict):
        """
        Usage
        -----
        While logging in, verify email and password
        Also verify if user exists
        If exists check password

        Parameters
        ----------
        details: email and password in dict

        Returns
        -------

        """
        # verify email
        # verify password
        # return status
        return True

    def verify_register_form(self, details: dict):
        """
        Usage
        -----
        verify user email, password while creating new account

        Parameters
        ----------
        details: dict

        Returns
        -------
        return boolean status

        """
        # verify email
        if not self.is_email_valid(details["email"]):
            return False

        # verify password
        if not self.is_password_valid(details["password"]):
            return False

        # verify retyped password
        if not self.is_password_valid(details["retype_password"]):
            return False

        # verify retyped password is same as password
        if not (details["password"] == details["retype_password"]):
            return False

        return True

    def generate_web_token(self, email: str, token_expiry_on: int) -> str:
        """
        Usage
        -----
        Generate jwt token from email id

        Parameters
        ----------
        email : email id of user
        token_expiry_on : expiry timestamp

        Returns
        -------
        web_token

        """
        # use current time stamp and email to generate unique token
        web_token = jwt.encode(
            {
                "email": email,
                "expiry": token_expiry_on,
            },
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return web_token

    def update_auth_table(self, user=None, details: dict = {}, user_id=None):
        """
        Usage
        -----
        Update auth table while logging in and creating new account

        Parameters
        ----------
        details : dict with user details
        user : user object before update
        user_id : user id while creating new account

        Returns
        -------
        updated user object

        """
        if details["operation"] == "login":
            user.web_token = details["web_token"]
            user.is_logged = True
            user.token_created_on = time.time()
            user.token_expiry_on = details["token_expiry_on"]

        if details["operation"] == "register":
            user = Auth(
                user_id=user_id,
                email=details["email"],
                password=details["password"],
                role=details["role"],
                first_name=details["first_name"],
                last_name=details["last_name"],
            )
            db.session.add(user)

        db.session.commit()
        return user


# --------------------  END  --------------------
