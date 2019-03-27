#!/bin/sh

docker kill $(docker ps -a -q -f status=running)
docker rm $(docker ps -a -q -f status=exited)
docker build -t webapp-image:v1 .
docker run -d -p 80:80 webapp-image:v1
