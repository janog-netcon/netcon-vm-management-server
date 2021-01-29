import unittest
import os

from nginx import build_config_filepath
from nginx import add_domain
from nginx import remove_domain


class TestNginxMethods(unittest.TestCase):
    def test_add_domain(self):
        add_domain("subdomain1.example.com", ["10.0.0.1"])

        path = build_config_filepath("subdomain1.example.com")

        with open(path) as f:
            content = f.read()

        self.assertEqual(
            content,
            """\
upstream subdomain1.example.com {
    server 10.0.0.1;
}

server {
    listen 80;
    server_name subdomain1.example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name subdomain1.example.com;

    ssl_certificate     /etc/nginx/certs/server.crt;
    ssl_certificate_key /etc/nginx/certs/server.key;

    location / {
        proxy_pass http://subdomain1.example.com;

        proxy_connect_timeout 5;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}""",
        )

    def test_remove_domain(self):
        add_domain("subdomain2.example.com", ["10.1.1.1", "10.1.1.2"])

        remove_domain("subdomain2.example.com")

        path = build_config_filepath("subdomain2.example.com")

        self.assertFalse(os.path.exists(path))


if __name__ == "__main__":
    unittest.main()
