import string
import random
import socket
from flask import Flask, Blueprint, json
from werkzeug.exceptions import HTTPException
from src.controller import vm_management_controller

app = Flask(__name__)
app.register_blueprint(vm_management_controller.app)

socket.setdefaulttimeout(10)

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps(
        {
            "error": {
                "code": e.code,
                "name": e.name,
                "description": e.description
            }
        }
    )
    response.content_type = "application/json"
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0')

application = app
