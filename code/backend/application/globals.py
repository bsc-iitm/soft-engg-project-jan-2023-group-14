# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This file contains global constants and variables.

# --------------------  Imports  --------------------

import os

# --------------------  Code  --------------------

BACKEND_ROOT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
HOST = '127.0.0.1'
PORT = 5000
DEBUG = True
BASE = f'http://{HOST}:{PORT}'
API_VERSION = 'v1'
TOKEN_VALIDITY = 300 # seconds
ACCEPTED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif']
PROFILE_PIC_PATH = os.path.join(BACKEND_ROOT_PATH, 'databases', 'images', 'profile_pics')
TICKET_ATTACHMENTS_PATH = os.path.join(BACKEND_ROOT_PATH, 'databases', 'images', 'ticket_attachments')


# --------------------  END  --------------------
