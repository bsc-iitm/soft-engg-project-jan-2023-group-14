# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This is FAQ Blueprint file.

# --------------------  Imports  --------------------

from flask import Blueprint
from flask_restful import Api, Resource

# --------------------  Code  --------------------

faq_bp = Blueprint('faq_bp', __name__)
faq_api = Api(faq_bp)

class FAQAPI(Resource):
    def get(self):
        # get all faq and return
        return {'task': 'This is FAQ API : GET'}
    
    def post(self):
        # create a new faq
        return {'task': 'This is FAQ API : POST'}

faq_api.add_resource(FAQAPI, '/') # path is /api/v1/faq

# --------------------  END  --------------------
