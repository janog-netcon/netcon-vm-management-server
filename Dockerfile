FROM nginx:1.19.4

RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org flask && \
    pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org uwsgi && \
    pip3 install google-api-python-client && \
    pip3 install oauth2client && \
    pip3 install apscheduler && \
    pip3 install requests
RUN pip3 install uwsgi

RUN mkdir /var/app

COPY app.py /var/app
COPY src/ /var/app/src/
COPY env/creds.json /var/app/
COPY env/startup_script.sh /var/app/
COPY env/default.conf /etc/nginx/conf.d/default.conf
COPY env/uwsgi.ini /var/app/

CMD ["/bin/bash", "/var/app/startup_script.sh"]
