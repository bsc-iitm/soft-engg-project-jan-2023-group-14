# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This is Admin Blueprint file which contains
# Admin API and related methods.

# --------------------  Imports  --------------------

import hashlib
import time
from flask import Blueprint, request
from flask_restful import Api, Resource
from application.logger import logger
from application.common_utils import (
    token_required,
    users_required,
    convert_base64_to_img,
    convert_img_to_base64,
    is_img_path_valid,
    is_base64,
    get_encoded_file_details,
)
from application.views.user_utils import UserUtils
from application.responses import *
from application.models import *
from copy import deepcopy
from flask_cors import cross_origin
from application.globals import *
import base64

# --------------------  Code  --------------------

class AdminUtils(UserUtils):
    def __init__(self,user_id=None):
        self.user_id=user_id
    def convert_admin_to_dict(self, user) -> dict:
        user_dict = vars(user)  # verify if this properly converts obj to dict
        if "_sa_instance_state" in user_dict:
            del user_dict["_sa_instance_state"]
        print(f"\n\n{user_dict}\n\n")
        return user_dict

admin_bp = Blueprint("admin_bp", __name__)
admin_api = Api(admin_bp)
admin_util=AdminUtils()

class AdminAPI(Resource):
    def get(self,user_id):
        """
        Usage
        -----
        Get a details of admin from user_id

        Parameters
        ----------
        user id

        Returns
        -------
        details

        """
        if admin_util.is_blank(user_id):
            raise BadRequest(status_msg="User id is missing.")

        # check if user exists
        try:
            user = Auth.query.filter_by(user_id=user_id).first()
        except Exception as e:
            logger.error(
                f"AdminAPI->get : Error occured while fetching admin data : {e}"
            )
            raise InternalServerError
        else:
            if user:
                if user.role == "admin":

                    admin_dict = admin_util.convert_admin_to_dict(
                        user
                    )  # NOT TESTED
                    return success_200_custom(data=admin_dict)
                else:
                    # User should be support staff
                    raise BadRequest(
                        status_msg="User must be a Admin."
                    )

            else:
                raise NotFoundError(status_msg="Admin does not exists")

# test case -> should not give details of student and support staff
    # @token_required
    # @users_required(users=["admin"])
    def put(self,user_id):
        """
        Usage
        ------
        Update admin profile,
        #admin can update first name, last name, email, password, profile picture location
        ------
        Args:
            user_id (integer): id of user
        ------
        Parameters
        ------
        Form data send with request
        
        Returns
        ------
        """
        details = {
            "first_name": "",
            "last_name": "",
            "email": "",
            "password": "",
            "profile_photo_loc": "",
        }
    
        # check url data
        if admin_util.is_blank(user_id):
            raise BadRequest(status_msg="User id is missing.")
            
        # checks form data 
        try:
            form = request.get_json()
            for key in details:
                value = form.get(key, "")
                if admin_util.is_blank(value):
                    value = ""
                details[key] = value
        except Exception as e:
            logger.error(
                f"AdminAPI->put : Error occured while getting form data : {e}"
            )
            raise InternalServerError

        # check if user exists
        try:
            user=Auth.query.filter_by(user_id=user_id).first()
        except Exception as e:
            logger.error(
                f"AdminAPI->get : Error occured while fetching user data : {e}"
            )
            raise InternalServerError
        else:
            # User doesn't exist
            if not user:
                raise NotFoundError(status_msg="User does not exists")

            role = user.role

            if role == "admin":

                # checks if email is valid
                if not (admin_util.is_email_valid(details["email"])):
                    raise BadRequest(
                            status_msg=f"Email is required annd should be correct"
                        )
                else:
                    user2=Auth.query.filter_by(email=details["email"]).first()
                    
                    # checks if another user already exist with same user id 
                    if user2.user_id!=user.user_id:
                        raise AlreadyExistError(status_msg="Email is already in use")
                    else:
                        user.email=details["email"]

                # checks if first name is empty
                if admin_util.is_blank(details["first_name"]):
                    raise BadRequest(
                            status_msg=f"First Name is required"
                        )
                else:
                    user.first_name=details["first_name"]

                # checks if last is empty
                if admin_util.is_blank(details["last_name"]):
                    raise BadRequest(
                            status_msg=f"Last Name is required"
                        )
                else:
                    user.last_name=details["last_name"]


                # checks is password is in correct format
                if not (admin_util.is_password_valid(details["password"])):
                    raise BadRequest(
                            status_msg=f"password is required annd should be in correct format"
                        )
                else:
                    user.password=details["password"]

                user.profile_photo_loc=details["profile_photo_loc"]

                try:
                    # db.session.add(ticket)
                    db.session.commit()
                except Exception as e:
                    logger.error(
                        f"AdminAPI->post : Error occured while updating admin details : {e}"
                    )
                    # TODO: db rollback not added yet
                    raise InternalServerError(
                        status_msg="Error occured while updating admin details"
                    )
                else:
                    logger.info("Admin details Updated successfully.")
                    raise Success_200(status_msg="Admin details Updated successfully.")
  
            else:
                # User should be support staff
                raise BadRequest(
                    status_msg="User must be a Admin."
                )


admin_api.add_resource(AdminAPI, '/<string:user_id>')  # path is /api/v1/admin

# --------------------  END  --------------------
