import json
from flask import Flask, abort
from googleapiclient import discovery
from googleapiclient import errors
from oauth2client.client import GoogleCredentials

from src import config
from src.generator import string_generator
from src.client.startup_script import create_startup_script
from src.client.dto.instances_list_response import instances_list_response

flask = Flask(__name__)    

def get_service_by_version(version):
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', version, credentials=credentials)
    return service

def get_instance(instance_name, project, zone):
    service = get_service_by_version('v1')
    request = service.instances().get(project=project, zone=zone, instance=instance_name)
    try:
        response = request.execute()
    except errors.HttpError as err:
        flask.logger.error("gce_client error : " + str(err.resp.status) + " " + str(err._get_reason()))  
        abort(err.resp.status, str(err._get_reason()))
        """ 
        raise SystemError({
            "error": {
                "code": err.resp.status,
                "description": err._get_reason()
            }
        })
        """
    return response

def get_instances(project, zone):
    service = get_service_by_version('v1')
    request = service.instances().list(project=project, zone=zone)
    response_list = []
    while request is not None:
        try:
            response = request.execute()
        except errors.HttpError as err:
            flask.logger.error("gce_client error : " + str(err.resp.status) + " " + str(err._get_reason()))
            abort(err.resp.status, str(err._get_reason()))
            """
            raise SystemError({
                "error": {
                    "code": err.resp.status,
                    "description": err._get_reason()
                }
            })
            """
        if 'items' in response:
            for instance in response['items']:
                # [Minor] TODO : Need to extract "name": "external-IP" from accessConfigs
                if 'natIP' in instance['networkInterfaces'][0]['accessConfigs'][0] :
                    response_list.append(
                        instances_list_response(instance['id'], instance['name'], instance['status'], instance['networkInterfaces'][0]['accessConfigs'][0]['natIP']).toObject()
                    )
        request = service.instances().list_next(previous_request=request, previous_response=response)
    return response_list

def create_instance(machine_image_name, project, zone, user_id, password):
    service = get_service_by_version('beta')
    
    name = machine_image_name + "-" + string_generator.get_random_string(5).lower()
    script = create_startup_script(user_id, password)

    request_body = {
        "name": name,
        "sourceMachineImage": "https://www.googleapis.com/compute/v1/projects/" + project + "/global/machineImages/" + machine_image_name,
        "metadata": {
            "kind": "compute#metadata",
            "items": [
                {
                    "key": "startup-script",
                    "value": script
                }
            ]
        }
    }
    request = service.instances().insert(project=project, zone=zone, body=request_body)
    response = request.execute()
    flask.logger.debug("First VM insert response: " + str(response))
    response["name"] = name
    try:
        response = request.execute()
    except errors.HttpError as err:
        if err.resp.status == 409:
            flask.logger.debug("Second VM insert response: " + str(response))
            return response
        flask.logger.error("gce_client error : " + str(err.resp.status) + " " + str(err._get_reason()))    
    return response

def delete_instance(instance_name, project, zone):
    service = get_service_by_version('v1')
    request = service.instances().delete(project=project, zone=zone, instance=instance_name)
    try:
        response = request.execute()
    except errors.HttpError as err:
        flask.logger.error("gce_client error : " + str(err.resp.status) + " " + str(err._get_reason()))    
        abort(err.resp.status, str(err._get_reason()))
        """
        raise SystemError({
            "error": {
                "code": err.resp.status,
                "description": err._get_reason()
            }
        })
        """
    return response

def start_instance(instance_name, project, zone):
    service = get_service_by_version('v1')
    request = service.instances().start(project=project, zone=zone, instance=instance_name)
    try:
        response = request.execute()
    except errors.HttpError as err:
        flask.logger.error("gce_client error : " + str(err.resp.status) + " " + str(err._get_reason()))    
        abort(err.resp.status, str(err._get_reason()))
        """
        raise SystemError({
            "error": {
                "code": err.resp.status,
                "description": err._get_reason()
            }
        })
        """
    return response

def stop_instance(instance_name, project, zone):
    service = get_service_by_version('v1')
    request = service.instances().stop(project=project, zone=zone, instance=instance_name)
    try:
        response = request.execute()
    except errors.HttpError as err:
        flask.logger.error("gce_client error : " + str(err.resp.status) + " " + str(err._get_reason()))    
        abort(err.resp.status, str(err._get_reason()))
        """
        raise SystemError({
            "error": {
                "code": err.resp.status,
                "description": err._get_reason()
            }
        })
        """
    return response
