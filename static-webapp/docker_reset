#!/bin/sh

docker kill $(docker ps -a -q -f status=running)
docker rm $(docker ps -a -q -f status=exited)
docker build -t webserver-image:v1 .
docker run -d -p 80:80 webserver-image:v1
