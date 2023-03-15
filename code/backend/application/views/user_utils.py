# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This file contains user class (common).

# --------------------  Imports  --------------------

import re
from flask import current_app as app
import jwt
import hashlib

# --------------------  Code  --------------------


class UserUtils:
    def is_blank(self, string):
        # for "", "  ", None : True else False
        return not (bool(string and not string.isspace()))

    def is_email_valid(self, email):
        is_valid = False
        # regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        # is_valid = re.search(regex, email)
        if '@' in email:
            is_valid = True
        return is_valid

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
        print(details)
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

    def generate_user_id(self, email: str) -> str:
        """
        Usage
        -----
        Generate user id from email and hashing with md5

        Parameters
        ----------
        email : email id of user

        Returns
        -------
        user_id

        """
        # use email to generate unique id
        user_id = hashlib.md5(email.encode()).hexdigest()
        return user_id


# --------------------  END  --------------------
