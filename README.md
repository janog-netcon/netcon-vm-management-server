# netcon-vm-management-server
Please ask meu for creds.json if necessary (basically this can be downloaded from GCP)

## How to run the example scripts
- Download GCP API key as creds.json
- Set the key like below
```$ export GOOGLE_APPLICATION_CREDENTIALS=/path/to/creds.json```
- Run
```$ python gce_blah```


## How to build
```
# Build the container
$ docker-compose build

# Run the container
$ docker-compose up -d

# Try to send a request
$ curl http://127.0.0.1:8950/

$ curl -X POST http://127.0.0.1:8950/instance -d '{"machine_image_name":"eve-ng-permmit-ssh-pass-auth-machine-image"}' -H "Content-Type: application/json" -H "Authorization: Bearer bWV1QGdtYWlsLmNvbTozODU0MmZjMTEzZjUwMmIxNzRiOTM1Mjc0M2I4Nzg2YThmODk2ZTc5"

$ curl -X DELETE http://127.0.0.1:8950/instance?instance_name=eve-ng-permmit-ssh-pass-auth-machine-image-blah -H "Authorization: Bearer bWV1QGdtYWlsLmNvbTozODU0MmZjMTEzZjUwMmIxNzRiOTM1Mjc0M2I4Nzg2YThmODk2ZTc5"

# Enter the container
$ docker-compose exec flask /bin/bash

# Stop the container
$ docker-compose kill flask
```

| application | port |
| ----------- | ---- |
| API server  | 8950 |
| nginx       | 8951 |

## How to debug (memo)
```
[terminal]
$ docker-compose exec flask /bin/bash
...
root@c8edb2a1588b:/var/app# export FLASK_DEBUG=True
root@c8edb2a1588b:/var/app# flask run

[another terminal]
$ docker-compose exec flask /bin/bash
root@c8edb2a1588b:/# curl http://127.0.0.1:5000/health

[see uwsgi log for production]
$ cat /var/log/uwsgi.log
```
