# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This file contains auth related methods.

# --------------------  Imports  --------------------

# from flask import Blueprint
# from flask_restful import Api, Resource
# from application.logger import logger

# --------------------  Code  --------------------

class AuthUtils:

    def __init__(self, user_id=None):
        self.user_id = user_id

    def __repr__(self) -> str:
        return f'Auth_Utils object for user: {self.user_id}'

    def verify_user_details(details:dict):
        """
        Usage
        -----

        Parameters
        ----------

        Returns
        -------
        
        """
        # verify email
        # verify password
        # return status
        return True

    def generate_web_token(user_email:str):
        """
        Usage
        -----

        Parameters
        ----------

        Returns
        -------
        
        """
        # use current time stamp and email to generate unique token
        # return token
        return ''


# --------------------  END  --------------------
