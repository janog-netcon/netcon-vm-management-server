import json
import base64
from flask import abort
from src import config

acceptable_email_list = [
    "meu@gmail.com"
]

def validate(request_headers):
    if 'Authorization' not in request_headers or validate_authorization(request_headers['Authorization']) == False:
        abort(400)

def validate_authorization(authorization):
    return authorization in ["Bearer " + base64.b64encode((email + ":" + config.api_token).encode('utf-8')).decode('utf-8') for email in acceptable_email_list]