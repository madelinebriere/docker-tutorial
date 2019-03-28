#!/bin/sh

docker kill $(docker ps -a -q -f status=running)
docker rm $(docker ps -a -q -f status=created)
docker rm $(docker ps -a -q -f status=exited)
docker build -t mapreduce-image:v1 .
docker run -v /var/run/docker.sock:/var/run/docker.sock mapreduce-image:v1