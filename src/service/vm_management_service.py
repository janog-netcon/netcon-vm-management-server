import time
import json
import string
import random
from flask import Flask, Response, abort
from src.client import gce_client, db_client
from src.nginx import nginx
from src.generator import string_generator
from src import config

flask = Flask(__name__)

def get_instances():
    get_problem_environments_response = db_client.get_problem_environments()
    response = []
    for content in get_problem_environments_response:
        response.append(
            {
                "instance_name": content['name'],
                "machine_image_name": content['machine_image_name'],
                "domain": content['host'],
                "project": content['project'],
                "zone": content['zone'],
                "status": content['status'],
                "problem_id": content['problem_id'],
                "user_id": content['user'],
                "password": content['password']
            }
        )
    return {
        "response": response
    }

def get_instances_by_name(instance_name):
    get_problem_environments_by_name_response = db_client.get_problem_environments_by_name(instance_name)
    response = []
    for content in get_problem_environments_by_name_response:
        response.append(
            {
                "instance_name": content['name'],
                "machine_image_name": content['machine_image_name'],
                "domain": content['host'],
                "project": content['project'],
                "zone": content['zone'],
                "status": content['status'],
                "problem_id": content['problem_id'],
                "user_id": content['user'],
                "password": content['password']
            }
        )
    return {
        "response": response
    }

def get_gce_instances(project, zone):
    get_instances_response = gce_client.get_instances(project, zone)
    response = []
    for content in get_instances_response:
        response.append(
            {
                "instance_name": content['name'],
                "status": content['status']
            }
        )
    return {
        "response": response
    }

def create_instance(machine_image_name, project, zone, problem_id):
    user_id = "janoger"
    password = string_generator.get_random_string_with_symbol(8)

    response = gce_client.create_instance(machine_image_name, project, zone, user_id, password)

    domain = string_generator.get_random_string(8) + config.get_proxy_domain_suffix()

    # external ip will not be issued at the creation moment, will do pooling (maybe it takes 3-4 sec.)
    for _ in range(10):
        get_instance_response = gce_client.get_instance(response['name'], project, zone)
        if 'natIP' in get_instance_response['networkInterfaces'][0]['accessConfigs'][0]:
            break
        time.sleep(1)

    if 'natIP' not in get_instance_response['networkInterfaces'][0]['accessConfigs'][0]:
        delete_instance(response['name'], project, zone)
        abort(500, "external_ip is not found")

    try:
        external_ip = get_instance_response['networkInterfaces'][0]['accessConfigs'][0]['natIP']
        nginx.add_domain(domain, [external_ip])
    except:
        flask.logger.error("failed to add nginx domain file")

    try:
        db_client.post_problem_environments(problem_id, response['name'], machine_image_name, response['status'], user_id, password, external_ip, project, 50080, 'SSH', zone)
        #db_client.post_problem_environments(problem_id, response['name'], machine_image_name, response['status'], user_id, password, domain, project, 443, 'HTTPS', zone)
    except:
        flask.logger.error("failed to update DB" + str(response))
        delete_instance(response['name'], project, zone)
        abort(500, "db cannot be updated")

    return {
        "response": {
            "instance_name": response['name'],
            "machine_image_name": machine_image_name,
            "domain": domain,
            "project": project,
            "zone": zone,
            "status": response['status'],
            "problem_id": problem_id,
            "user_id": user_id,
            "password": password
        }
    }

def delete_instance(instance_name, project, zone):
    get_problem_environments_by_name = db_client.get_problem_environments_by_name(instance_name)
    try:
        nginx.remove_domain(get_problem_environments_by_name[0]['host'])
    except:
        flask.logger.error("failed to delete nginx config")

    db_client.delete_problem_environments(instance_name)

    gce_client.delete_instance(instance_name, project, zone)

    return {
        "response": {
            "is_deleted": "true"
        }
    }

def reboot_instance(instance_name, project, zone):
    try:
        gce_client.stop_instance(instance_name, project, zone)
    except:
        flask.logger.error("failed to stop instance")
    gce_client.start_instance(instance_name, project, zone)  
    return {
        "response": {
            "is_rebooted": "true"
        }
    }
