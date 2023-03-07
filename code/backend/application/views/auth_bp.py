# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This file contains Login/Logout/Register API.

# --------------------  Imports  --------------------

from flask import Blueprint
from flask_restful import Api, Resource
from application.logger import logger
from application.views.auth_utils import AuthUtils

# --------------------  Code  --------------------

auth_bp = Blueprint('auth_bp', __name__)
auth_api = Api(auth_bp)
auth_utils = AuthUtils() # pass user_id for init

class Login(Resource):
    def post(self):
        """
        Usage
        -----

        Parameters
        ----------

        Returns
        -------
        
        """
        # get form data
        # verify form data
        # generate token
        # update auth table
        # return succes/error msg
        logger.info('Logged in')
        return "This is Auth API Login page"


class Register(Resource):
    def post(self):
        """
        Usage
        -----

        Parameters
        ----------

        Returns
        -------
        
        """
        # get form data
        # verify form data
        # verify if user exists
        # generate token
        # update auth table
        # return succes/error msg
        return "This is Auth API Register page"


class NewUsers(Resource):
    def get(self):
        """
        Usage
        -----

        Parameters
        ----------

        Returns
        -------
        
        """
        # get new users data from auth table
        # convert to dict
        # return succes/error msg with dict
        return 
    
    def put(self):
        """
        Usage
        -----

        Parameters
        ----------

        Returns
        -------
        
        """
        # update auth table for passed verification
        # return succes/error msg
        return 
    
    def delete(self):
        """
        Usage
        -----

        Parameters
        ----------

        Returns
        -------
        
        """
        # update auth table for failed verification
        # return succes/error msg
        return 


auth_api.add_resource(Login, '/login') # path is /api/v1/auth
auth_api.add_resource(Register, '/register')
auth_api.add_resource(NewUsers, '/newUsers')

# --------------------  END  --------------------
