# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This file contains Login/Logout/Register API.

# --------------------  Imports  --------------------

from flask import Blueprint, request
from flask import current_app as app
from flask_restful import Api, Resource
from application.logger import logger
from application.views.auth_utils import AuthUtils
from application.responses import *
from flask_login import login_user, login_required, logout_user
import jwt
from datetime import datetime, timedelta
from application.models import Auth
from application.globals import TOKEN_VALIDITY
from application.database import db
import time

# --------------------  Code  --------------------

auth_bp = Blueprint("auth_bp", __name__)
auth_api = Api(auth_bp)
auth_utils = AuthUtils()  # pass user_id for init


class Login(Resource):
    def post(self):
        """
        Usage
        -----
        For the user login page. It checks user data and raise appropriate error
        if required. Else it generates user token and returns it.

        Parameters
        ----------
        form data sent with request
        data format {'email':'', 'password':''}

        Returns
        -------
        User web token

        """
        form = {}

        # get form data
        try:
            form = request.get_json()
            email = form.get("email", "")
            password = form.get("password", "")

            if auth_utils.is_blank(email) or auth_utils.is_blank(password):
                raise BadRequest(status_msg=f"Email or Password is empty")

            details = {"email": email, "password": password}
        except Exception as e:
            logger.error(f"Login->post : Error occured while getting form data : {e}")
            raise InternalServerError
        else:
            # verify form data
            if auth_utils.is_email_valid(email) and auth_utils.is_password_valid(
                password
            ):
                # check if user exists

                user = Auth.query.filter_by(email=email).first()
                if user:
                    # user exists
                    user_id = user.user_id

                    if password == user.password:
                        # password is correct so log in user
                        login_user(user, remember=True)

                        # generate token
                        token_expiry_on = time.time() + TOKEN_VALIDITY
                        web_token = auth_utils.generate_web_token(
                            email, token_expiry_on
                        )

                        # update auth table
                        user = auth_utils.update_auth_table(
                            user,
                            details={
                                "web_token": web_token,
                                "operation": 'login',
                                "token_expiry_on": token_expiry_on,
                            },
                        )

                        logger.info("User logged in.")
                        return success_200_custom(
                            data={
                                "user_id": user_id,
                                "web_token": web_token,
                                "token_expiry_on": token_expiry_on,
                            }
                        )

                    else:
                        # password is wrong
                        raise Unauthenticated(status_msg="Password is incorrect")
                else:
                    # user does not exists
                    raise NotFoundError(status_msg="User does not exists")
            else:
                # email or password are not valid as per specification
                raise BadRequest(
                    status_msg="Email or Password are not valid as per specification"
                )


class Register(Resource):
    def post(self):
        """
        Usage
        -----
        For the user register page. It checks user data and raise appropriate error
        if required. Created user account and it generates user token and returns it.

        Parameters
        ----------
        form data sent with request
        data format {'first_name':'', 'last_name':'', 'email':'',
                    'password':'', 'retype_password':'', 'role':''}

        Returns
        -------
        User web token

        """
        form = {}
        details = {
            "first_name": "",
            "last_name": "",
            "email": "",
            "password": "",
            "retype_password": "",
            "role": "",
        }

        # get form data
        try:
            form = request.get_json()
            for key in details:
                value = form.get(key, "")
                details[key] = value
                if auth_utils.is_blank(value):
                    raise BadRequest(status_msg=f"{key} is empty or invalid")
            details['operation'] = 'register'
        except Exception as e:
            logger.error(
                f"Register->post : Error occured while getting form data : {e}"
            )
            raise InternalServerError
        else:
            # verify registration form data
            if auth_utils.verify_register_form(details):
                # check if user exists
                user = Auth.query.filter_by(email=details["email"]).first()
                if user:
                    # user exists means email is already in use
                    raise AlreadyExistError(status_msg="Email is already in use")
                else:
                    # generate unique user_id
                    user_id = "blablabla"+str(int(time.time()))  # function not yet implemented

                    # create new user in Auth table
                    user = auth_utils.update_auth_table(user_id=user_id, details=details)

                    # Redirect to login page in frontend
                    # No need to create web_token as during login it will
                    # be created

                    logger.info("New account created")
                    raise Success_200(status_msg="Account created successfully. Now please login.")      

            else:
                # email or password are not valid as per specification
                raise BadRequest(
                    status_msg="Email or Password are not valid as per specification OR Password did not match."
                )


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


auth_api.add_resource(Login, "/login")  # path is /api/v1/auth
auth_api.add_resource(Register, "/register")
auth_api.add_resource(NewUsers, "/newUsers")

# --------------------  END  --------------------
