# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This is Student Blueprint file which contains 
# Student API and related methods.

# --------------------  Imports  --------------------

from flask import Blueprint
from flask_restful import Api, Resource, url_for

# --------------------  Code  --------------------

student_bp = Blueprint('student_bp', __name__)
student_api = Api(student_bp)

@student_bp.route('/custom_student_task') # path is /api/v1/student/custom_student_task
def index():
    return "This is student blueprint home page"

class StudentAPI(Resource):
    def get(self):
        return {'task': 'Say "Hello, World!" on Student API'}

student_api.add_resource(StudentAPI, '/') # path is /api/v1/student

# --------------------  END  --------------------
