# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This is Support Staff Blueprint file.

# --------------------  Imports  --------------------

from flask import Blueprint
from flask_restful import Api, Resource

# --------------------  Code  --------------------

support_bp = Blueprint('support_bp', __name__)
support_api = Api(support_bp)

class SupportAPI(Resource):
    def get(self):
        return {'task': 'This is Support API'}

support_api.add_resource(SupportAPI, '/') # path is /api/v1/support

# --------------------  END  --------------------
