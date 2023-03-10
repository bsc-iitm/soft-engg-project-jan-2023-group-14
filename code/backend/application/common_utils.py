# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This is common utils file. All common and independent functions will be here.

# --------------------  Imports  --------------------

from functools import wraps
from flask import request
from application.responses import *
from application.logger import logger
# from flask_login import current_user
from application.models import Auth
# from application import login_manager

# --------------------  Code  --------------------

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            frontend_token = request.headers.get('web_token', '')
            user_id_rec = request.headers.get('user_id', '') # user_id sent by frontend
        except Exception as e:
            logger.error(f'Error occured while checking request token : {e}')
            raise InternalServerError
        else:
            user = Auth.query.filter_by(user_id=user_id_rec).first()
            if user:
                if user.is_logged:
                    if frontend_token:
                        # check token
                        backend_token = user.web_token
                        if frontend_token == backend_token:
                            # token is correct
                            print("\n\n Token is verified \n\n")
                            return f(*args, **kwargs) 
                        else:
                            raise Unauthenticated(status_msg="Token is incorrect")
                    else:
                        # token is empty
                        raise Unauthenticated(status_msg="Token is empty or missing")
                else:
                    raise Unauthenticated(status_msg="Access denied. User is not logged in.")
            else:
                raise NotFoundError(status_msg="Provided used id does not exists. Please create account.")    
    return decorated


# TODO: CONVERT MULTIPLE DECORATORS TO ONE USING ARGS ?? NOT IMPLEMENTED YET

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            user_id_rec = request.headers.get('user_id', '') # user_id sent by frontend
        except Exception as e:
            logger.error(f'Error occured while checking user id : {e}')
            raise InternalServerError
        else:
              role = Auth.query.filter_by(user_id = user_id_rec).first().role
              if role == "admin":
                  # role verified
                  print("\n\n Admin role is verified \n\n")
                  return f(*args, **kwargs) 
              else:
                  raise Unauthenticated(status_msg="Access denied. Only admin can access this endpoint.")
    return decorated


def support_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            user_id_rec = request.headers.get('user_id', '') # user_id sent by frontend
        except Exception as e:
            logger.error(f'Error occured while checking user id : {e}')
            raise InternalServerError
        else:
              role = Auth.query.filter_by(user_id = user_id_rec).first().role
              if role == "support":
                  # role verified
                  print("\n\n Support role is verified \n\n")
                  return f(*args, **kwargs) 
              else:
                  raise Unauthenticated(status_msg="Access denied. Only Support Staff can access this endpoint.")
    return decorated


def student_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            user_id_rec = request.headers.get('user_id', '') # user_id sent by frontend
        except Exception as e:
            logger.error(f'Error occured while checking user id : {e}')
            raise InternalServerError
        else:
              role = Auth.query.filter_by(user_id = user_id_rec).first().role
              if role == "student":
                  # role verified
                  print("\n\n Student role is verified \n\n")
                  return f(*args, **kwargs) 
              else:
                  raise Unauthenticated(status_msg="Access denied. Only Studnet can access this endpoint.")
    return decorated



def users_required(users):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                user_id_rec = request.headers.get('user_id', '') # user_id sent by frontend
            except Exception as e:
                logger.error(f'Error occured while checking user id : {e}')
                raise InternalServerError
            else:
                user = Auth.query.filter_by(user_id = user_id_rec).first()
                if user:
                    role = user.role
                    if role in users:
                        # role verified
                        print(f"\n\n {role} role is verified \n\n")
                        return f(*args, **kwargs) 
                    else:
                        raise Unauthenticated(status_msg="Access denied.")
                else:
                    raise NotFoundError(status_msg="User does not exists")
        return decorated
    return decorator


# --------------------  END  --------------------
