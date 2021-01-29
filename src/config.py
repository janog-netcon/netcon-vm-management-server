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
        ('janog47-netcon-dev', 'asia-northeast1-a'),
        ('janog47-netcon-dev', 'asia-northeast1-b'),
        ('janog47-netcon-dev', 'asia-northeast1-c')
    ]

# db settings
host_db = 'http://netcon-score-server_vmdb-api_1:8080'

connection_timeout = 3.0
read_timeout = 10.0
retries = 5

# scheduler settings
synchronizer_seconds = 20

# wrapper for config variables
def get_proxy_domain_suffix():
    if env == "PROD":
        return ".proxy.netcon.janog.gr.jp"
    else :
        return ".proxy-dev.netcon.janog.gr.jp"
