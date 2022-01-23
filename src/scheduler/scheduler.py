import time
import atexit
import datetime
from datetime import timezone
from src import config
from src.client import gce_client, db_client
from src.service import vm_management_service
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

flask = Flask(__name__)

def synchronizer():
    for project_zone_tupple in config.project_zone_list:
        project = project_zone_tupple[0]
        zone = project_zone_tupple[1]
        flask.logger.warning("sync : " + project+ " " + zone)
        sync(project, zone)

def set_inner_status_for_preparing(problem_environment):
    """
    vm instanciate time
      "created_at":"2022-01-24T00:34:56.227757Z"
    vm
      NOT_READY -> READY if created_at + minutes >= now

    """
    created_at = datetime.datetime.strptime(problem_environment['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z')
    minutes = config.wait_duration_minutes_dict(problem_environment['machine_image_name'])

    if datetime.datetime.now >= datetime.datetime.timedelta(minutes=minutes) and problem_environment['status'] == 'READY':
        return 'READY'
    else:
        # inner
        return problem_environment['status']

def sync(project, zone):
    try:
        get_instances_response = vm_management_service.get_gce_instances(project, zone)
        if get_instances_response['response']:
            get_instances_instance_name_set = set(e['instance_name'] for e in get_instances_response['response'])
        else:
            get_instances_instance_name_set = set()
            flask.logger.warning(get_instances_response)
    except:
        get_instances_instance_name_set = set()
        flask.logger.error("failed to call GET /instances")

    try:
        get_problem_environments_response = vm_management_service.get_instances()
        problem_environments_instance_name_set = set(e['instance_name'] for e in get_problem_environments_response['response'])
    except:
        problem_environments_instance_name_set = set()
        flask.logger.error("failed to call GET /problem_environments")

    flask.logger.warning("VM and DB has " + str(get_instances_instance_name_set.intersection(problem_environments_instance_name_set)))

    # if instance exists in both of VM and DB
    for instance_name in get_instances_instance_name_set.intersection(problem_environments_instance_name_set):
        try:
            gce_instance = [x for x in get_instances_response['response'] if x['instance_name'] == instance_name][0]
        except:
            flask.logger.error(str(instance_name) + " not found on gce environment")
            continue
        if gce_instance['status'] in ['REPAIRING', 'TERMINATED', 'STOPPING']:
            flask.logger.warning(str(gce_instance['instance_name']) + " is unstable status : " + str(gce_instance['status']))
        try:
            problem_environment = [x for x in get_problem_environments_response['response'] if x['instance_name'] == instance_name][0]
        except:
            flask.logger.error(str(instance_name) + " not found on db")
            continue

        """
        vm instanciate time
          "created_at":"2022-01-24T00:34:56.227757Z"
        vm

        """
        created_at = datetime.datetime.strptime(problem_environment['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z')
        minutes = config.wait_duration_minutes_dict[problem_environment['machine_image_name']]

        future = created_at + datetime.timedelta(minutes=minutes)
        now = datetime.datetime.now(timezone.utc)

        # now
        if (now < future) and gce_instance['status'] == 'RUNNING':
           flask.logger.warning("not sync before running" + str(instance_name))
           continue

        if gce_instance['status'] != problem_environment['status']:
            try:
                flask.logger.warning("sync " + str(instance_name) + " status diff vm=" + str(gce_instance['status']) + " db="+ str(problem_environment['status']))
                db_client.post_problem_environments(
                    problem_id=problem_environment['problem_id'],
                    name=problem_environment['instance_name'],
                    machine_image_name=problem_environment['machine_image_name'],
                    status=gce_instance['status'],
                    user=problem_environment['user_id'],
                    password=problem_environment['password'],
                    host=problem_environment['domain'],
                    project=problem_environment['project'],
                    zone=problem_environment['zone'],
                    service='SSH',
                    port=50080
                )
                """
                db_client.post_problem_environments(
                    problem_id=problem_environment['problem_id'],
                    name=problem_environment['instance_name'],
                    machine_image_name=problem_environment['machine_image_name'],
                    status=gce_instance['status'],
                    user=problem_environment['user_id'],
                    password=problem_environment['password'],
                    host=problem_environment['domain'],
                    project=problem_environment['project'],
                    zone=problem_environment['zone'],
                    service='HTTPS',
                    port=443
                )
                """
                flask.logger.warning("sync successfully done : " + str(instance_name))
            except:
                flask.logger.error("failed to call POST /problem_environments")

    # if instance only exists in DB
    flask.logger.warning("VM only has " + str(get_instances_instance_name_set.difference(problem_environments_instance_name_set)))
            # Have decided not to make any changes
            #if instance['status'] in ['PROVISIONING', 'STAGING']:
            #    gce_client.delete_instance(instance)
            #else:
            #    flask.logger.warning("DB only has " + str(instance))

    # if instance only exists in VM
    flask.logger.warning("DB only has " + str(problem_environments_instance_name_set.difference(get_instances_instance_name_set)))

scheduler = BackgroundScheduler()
scheduler.add_job(func=synchronizer, trigger="interval", seconds=config.synchronizer_seconds)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
