#!/bin/sh

set -x

cd $(dirname $0)
docker build -t kyontan/netcon-score-server:vm-management-service .
cd ../netcon-score-server

docker-compose up -d vm-management-service
