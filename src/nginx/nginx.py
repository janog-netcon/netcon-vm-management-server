import os
import subprocess
from typing import List

from jinja2 import Template


TEMPLATE = """\
upstream {{ domain }} {
    server {{ upstream }};
}

server {
    listen 80;
    server_name {{ domain }};

    location / {
        proxy_pass http://{{ upstream }};

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Server $host;
    }
}
"""

NGINX_CONF_DIR = "/etc/nginx/conf.d/"


def build_config_filepath(domain: str) -> str:
    return os.path.join(NGINX_CONF_DIR, domain + ".conf")


def add_domain(domain: str, upstreams: List[str]) -> None:

    # nginxのテンプレート生成
    template = Template(TEMPLATE)
    config = template.render(
        upstream=upstreams[0],
        domain=domain,
    )

    # export
    with open(build_config_filepath(domain), "w") as f:
        f.write(config)

    # reload nginx
    args = ["nginx", "-s", "reload"]
    try:
        subprocess.run(
            args,
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        print("Error: ", e.stderr)


def remove_domain(domain: str) -> None:
    path = build_config_filepath(domain)
    try:
        os.remove(path)
    except FileNotFoundError:
        pass
