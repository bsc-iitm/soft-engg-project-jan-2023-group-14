# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This is Admin Blueprint file which contains 
# Admin API and related methods.

# --------------------  Imports  --------------------

from flask import Blueprint
from flask_restful import Api, Resource, url_for


# --------------------  Code  --------------------

admin_bp = Blueprint('admin_bp', __name__)
admin_api = Api(admin_bp)


class AdminAPI(Resource):
    def get(self):
        return {'task': 'Say "Hello, World!" on Admin API'}

admin_api.add_resource(AdminAPI, '/') # path is /api/v1/admin

# --------------------  END  --------------------
