import json
from flask import Flask, Blueprint, request, Response, abort
from src.validator import request_validator
from src.service import vm_management_service
from src.scheduler import scheduler

app = Blueprint('controller', __name__)
flask = Flask(__name__)

def formatResponse(response, code):
    return Response(response=json.dumps(response, indent=2, ensure_ascii=False), status=code)

@app.route('/health', methods = ["GET"])
def get_health():
    flask.logger.warning('message')
    return formatResponse({"status": "OK"}, 200)

@app.route('/instance', methods = ["GET"])
def get_instances_controller():
    request_validator.validate(request.headers)
    flask.logger.warning('GET /instance: validation ok')
    return formatResponse(vm_management_service.get_instances(), 200)

@app.route('/instance/<string:instance_name>', methods = ["GET"])
def get_instances_by_name_controller(instance_name):
    request_validator.validate(request.headers)
    flask.logger.warning('GET /instance/<string:instance_name>: validation ok')
    return formatResponse(vm_management_service.get_instances_by_name(instance_name), 200)

@app.route('/instance', methods = ["POST"])
def create_instance_controller():
    request_validator.validate(request.headers)
    machine_image_name = request.json['machine_image_name']
    problem_id = request.json['problem_id']
    project = request.json['project']
    zone = request.json['zone']
    return formatResponse(vm_management_service.create_instance(machine_image_name, project, zone, problem_id), 200)

@app.route('/instance/<string:instance_name>', methods = ["DELETE"])
def delete_instance_controller(instance_name):
    request_validator.validate(request.headers)
    project = request.json['project']
    zone = request.json['zone']
    return formatResponse(vm_management_service.delete_instance(instance_name, project, zone), 200)

@app.route('/reboot/<string:instance_name>', methods = ["POST"])
def reboot_instance_controller(instance_name):
    request_validator.validate(request.headers)
    project = request.json['project']
    zone = request.json['zone']
    return formatResponse(vm_management_service.reboot_instance(instance_name, project, zone), 200)

@app.route('/vm/instance', methods = ["GET"])
def get_vm_instances_controller():
    request_validator.validate(request.headers)
    project = request.args.get('project')
    zone = request.args.get('zone')
    return formatResponse(vm_management_service.get_gce_instances(project, zone), 200)
