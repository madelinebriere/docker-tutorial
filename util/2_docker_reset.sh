#!/bin/sh

running=$(docker ps -a -q -f status=running)
created=$(docker ps -a -q -f status=created)
exited=$(docker ps -a -q -f status=exited)
if [ -n "$running" ]
then
	echo "Killing container(s)."
	docker kill ${running}
fi
if [ -n "$created" ]
then
	echo "Removing created container(s)."
	docker rm ${created}
fi
if [ -n "$exited" ]
then
	echo "Removing exited container(s)."
	docker rm ${exited}
fi
docker build -t mapreduce-image:v1 .
docker run -v /var/run/docker.sock:/var/run/docker.sock mapreduce-image:v1