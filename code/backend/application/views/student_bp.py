# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This is Student Blueprint file which contains 
# Student API and related methods.

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

class StudentUtils(UserUtils):
    def __init__(self,user_id=None):
        self.user_id=user_id
    def convert_student_to_dict(self, user,tickets_created, tickets_voted) -> dict:
        user_dict = vars(user)  # verify if this properly converts obj to dict
        if "_sa_instance_state" in user_dict:
            del user_dict["_sa_instance_state"]
        user_dict["number_of_tickets_created"] = tickets_created
        user_dict["number_of_tickets_voted"] = tickets_voted
        print(f"\n\n{user_dict}\n\n")
        return user_dict

student_bp = Blueprint('student_bp', __name__)
student_api = Api(student_bp)
student_util=StudentUtils()

@student_bp.route('/custom_student_task') # path is /api/v1/student/custom_student_task
def index():
    return "This is student blueprint home page"

class StudentAPI(Resource):
    def get(self,user_id):
        """
        Usage
        -----
        Get a details of student from user_id

        Parameters
        ----------
        user id

        Returns
        -------
        details

        """
        if student_util.is_blank(user_id):
            raise BadRequest(status_msg="User id is missing.")

        # check if user exists
        try:
            user = Auth.query.filter_by(user_id=user_id).first()
        except Exception as e:
            logger.error(
                f"StudentAPI->get : Error occured while fetching ticket data : {e}"
            )
            raise InternalServerError
        else:
            if user:
                if user.role == "student":
                    number_of_tickets_created = Ticket.query.filter_by(created_by=user_id).count()
                    number_of_tickets_voted= TicketVote.query.filter_by(user_id=user_id).count()
                    student_dict = student_util.convert_student_to_dict(
                        user,number_of_tickets_created,number_of_tickets_voted
                    )  # NOT TESTED
                    return success_200_custom(data=student_dict)
                else:
                    # User should be student
                    raise BadRequest(
                        status_msg="User must be a student."
                    )

            else:
                raise NotFoundError(status_msg="Student does not exists")

# test case -> should not give details of support staff and admin
    # @token_required
    # @users_required(users=["student"])
    def put(self,user_id):
        """
        Usage
        ------
        Update student profile,
        #student can update first name, last name, email, password, profile picture location
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
        if student_util.is_blank(user_id):
            raise BadRequest(status_msg="User id is missing.")
            
        # checks form data 
        try:
            form = request.get_json()
            for key in details:
                value = form.get(key, "")
                if student_util.is_blank(value):
                    value = ""
                details[key] = value
        except Exception as e:
            logger.error(
                f"StudentAPI->put : Error occured while getting form data : {e}"
            )
            raise InternalServerError

        # check if user exists
        try:
            user=Auth.query.filter_by(user_id=user_id).first()
        except Exception as e:
            logger.error(
                f"StudentAPI->get : Error occured while fetching user data : {e}"
            )
            raise InternalServerError
        else:
            # User doesn't exist
            if not user:
                raise NotFoundError(status_msg="User does not exists")

            role = user.role

            if role == "student":

                # checks if email is valid
                if not (student_util.is_email_valid(details["email"])):
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
                if student_util.is_blank(details["first_name"]):
                    raise BadRequest(
                            status_msg=f"First Name is required"
                        )
                else:
                    user.first_name=details["first_name"]

                # checks if last is empty
                if student_util.is_blank(details["last_name"]):
                    raise BadRequest(
                            status_msg=f"Last Name is required"
                        )
                else:
                    user.last_name=details["last_name"]


                # checks is password is in correct format
                if not (student_util.is_password_valid(details["password"])):
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
                        f"StudentAPI->post : Error occured while updating student details : {e}"
                    )
                    # TODO: db rollback not added yet
                    raise InternalServerError(
                        status_msg="Error occured while updating student details"
                    )
                else:
                    logger.info("Student details Updated successfully.")
                    raise Success_200(status_msg="Stdent details Updated successfully.")
  
            else:
                # User should be student
                raise BadRequest(
                    status_msg="User must be a student."
                )


student_api.add_resource(StudentAPI, '/<string:user_id>') # path is /api/v1/student

# --------------------  END  --------------------