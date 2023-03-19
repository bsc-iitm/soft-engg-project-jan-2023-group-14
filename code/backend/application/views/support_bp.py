# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This is Support Staff Blueprint file.

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

class SupportUtils(UserUtils):
    def __init__(self,user_id=None):
        self.user_id=user_id
    def convert_support_to_dict(self, user,tickets_resolved) -> dict:
        user_dict = vars(user)  # verify if this properly converts obj to dict
        if "_sa_instance_state" in user_dict:
            del user_dict["_sa_instance_state"]
        user_dict["number_of_tickets_resolved"] = tickets_resolved
        print(f"\n\n{user_dict}\n\n")
        return user_dict

support_bp = Blueprint('support_bp', __name__)
support_api = Api(support_bp)
support_util = SupportUtils()

class SupportAPI(Resource):
    @token_required
    @users_required(users=["support"])
    def get(self,user_id):
        """
        Usage
        -----
        Get a details of support from user_id

        Parameters
        ----------
        user id

        Returns
        -------
        details

        """
        if support_util.is_blank(user_id):
            raise BadRequest(status_msg="User id is missing.")

        # check if user exists
        try:
            user = Auth.query.filter_by(user_id=user_id).first()
        except Exception as e:
            logger.error(
                f"SupportAPI->get : Error occured while fetching support data : {e}"
            )
            raise InternalServerError
        else:
            if user:
                if user.role == "support":

                    number_of_tickets_resolved = Ticket.query.filter_by(resolved_by=user_id).count()

                    support_dict = support_util.convert_support_to_dict(
                        user,number_of_tickets_resolved
                    )  # NOT TESTED
                    return success_200_custom(data=support_dict)
                else:
                    # User should be support staff
                    raise BadRequest(
                        status_msg="User must be a support staff."
                    )

            else:
                raise NotFoundError(status_msg="Support staff does not exists")

# test case -> should not give details of studenr and admin
    @token_required
    @users_required(users=["support"])
    def put(self,user_id):
        """
        Usage
        ------
        Update support profile,
        #support can update first name, last name, email, password, profile picture location
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
        if support_util.is_blank(user_id):
            raise BadRequest(status_msg="User id is missing.")
            
        # checks form data 
        try:
            form = request.get_json()
            for key in details:
                value = form.get(key, "")
                if support_util.is_blank(value):
                    value = ""
                details[key] = value
        except Exception as e:
            logger.error(
                f"SupportAPI->put : Error occured while getting form data : {e}"
            )
            raise InternalServerError

        # check if user exists
        try:
            user=Auth.query.filter_by(user_id=user_id).first()
        except Exception as e:
            logger.error(
                f"SupportAPI->get : Error occured while fetching user data : {e}"
            )
            raise InternalServerError
        else:
            # User doesn't exist
            if not user:
                raise NotFoundError(status_msg="User does not exists")

            role = user.role

            if role == "support":

                # checks if email is valid
                if not (support_util.is_email_valid(details["email"])):
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
                if support_util.is_blank(details["first_name"]):
                    raise BadRequest(
                            status_msg=f"First Name is required"
                        )
                else:
                    user.first_name=details["first_name"]

                # checks if last is empty
                if support_util.is_blank(details["last_name"]):
                    raise BadRequest(
                            status_msg=f"Last Name is required"
                        )
                else:
                    user.last_name=details["last_name"]


                # checks is password is in correct format
                if not (support_util.is_password_valid(details["password"])):
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
                        f"StudentAPI->post : Error occured while updating support staff details : {e}"
                    )
                    # TODO: db rollback not added yet
                    raise InternalServerError(
                        status_msg="Error occured while updating support staff details"
                    )
                else:
                    logger.info("Support Staff details Updated successfully.")
                    raise Success_200(status_msg="Support Staff details Updated successfully.")
  
            else:
                # User should be support staff
                raise BadRequest(
                    status_msg="User must be a support staff."
                )


support_api.add_resource(SupportAPI, '/<string:user_id>') # path is /api/v1/support

# --------------------  END  --------------------
