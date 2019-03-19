#!/bin/sh

./fetch_data.sh
docker kill $(docker ps -a -q -f status=running)
docker rm $(docker ps -a -q -f status=exited)
docker build -t mapreduce-image:v1 .
python docker_parallelize.py
