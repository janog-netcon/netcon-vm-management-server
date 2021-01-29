import json
import requests
from flask import Flask, abort
from src import config

flask = Flask(__name__)

def formatResponse(response):
    if response is not None and response.status_code in range(200, 300):
        return response.json()
    if response.status_code == 410:
        return {
            "error": {
                "code" : 410,
                "description": "Gone"
            }
        }
    else:
        flask.logger.error("db_client error : " + str(response.status_code))
        abort(response.status_code, "db_client error")
        """
        raise SystemError ({
            "error": {
                "code": response.status_code,
                "description": response.text
            }
        })
        """

def get_problem_environments():
    endpoint = '/problem-environments'
    response = requests.get(config.host_db + endpoint, timeout=(config.connection_timeout, config.read_timeout))
    return formatResponse(response)

def get_problem_environments_by_name(name):
    path_param = name
    endpoint = '/problem-environments/' + path_param
    response = requests.get(config.host_db + endpoint, timeout=(config.connection_timeout, config.read_timeout))
    return formatResponse(response)

def post_problem_environments(problem_id, name, machine_image_name, status, user, password, host, service, port, project, zone):
    endpoint = '/problem-environments'
    request_body = {
        'problem_id': problem_id,
        'name': name,
        'machine_image_name': machine_image_name,
        'status': status,
        'user': user,
        'password': password,
        'host': host,
        'project': project,
        'zone': zone,
        'service': service,
        'port': port
    }
    flask.logger.warning("request_body : " + str(request_body))
    response = requests.post(config.host_db + endpoint, json=request_body, headers={'Content-Type': 'application/json'}, timeout=(config.connection_timeout, config.read_timeout))
    return formatResponse(response)

def delete_problem_environments(name):
    path_param = name
    endpoint = '/problem-environments/' + path_param
    requests.delete(config.host_db + endpoint, timeout=(config.connection_timeout, config.read_timeout))
