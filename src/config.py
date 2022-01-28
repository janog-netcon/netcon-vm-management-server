# vm server settings
api_token = '38542fc113f502b174b9352743b8786a8f896e79'
env = "PROD"

# gce settings
if env == "PROD":
    project_zone_list = [
        ('networkcontest', 'asia-northeast1-b'),
        ('networkcontest', 'asia-northeast2-a'),
        ('networkcontest', 'asia-east1-b')
    ]
else:
    project_zone_list = [
        ('testing-environment-228409', 'asia-northeast1-b'),
        ('testing-environment-228409', 'asia-northeast2-a'),
        ('testing-environment-228409', 'asia-east1-b')
    ]

# db settings
host_db = 'http://vmdb-api:8080'

connection_timeout = 3.0
read_timeout = 10.0
retries = 5

# scheduler settings
synchronizer_seconds = 20

wait_duration_minutes_dict = {
  "image-aki-1": 5,
  "image-iys-1": 20,
  "image-kat1-1": 5,
  "image-kat2-2": 15,
  "image-nas-1": 10,
  "image-nemo-1": 5,
  "image-otsuka-1": 20,
  "image-shiozawa-1": 5,
  "image-takeda-1": 20,
  "image-tanioka1-1": 5,
  "image-tanioka2-2": 20,
  "image-abe-1": 5,
  "image-alisa-1": 15
}

# wrapper for config variables
def get_proxy_domain_suffix():
    if env == "PROD":
        return ".proxy.netcon.janog.gr.jp"
    else :
        return ".proxy-dev.netcon.janog.gr.jp"
