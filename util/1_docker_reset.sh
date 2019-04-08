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
docker build -t webapp-image:v1 .
docker run -d -p 80:80 webapp-image:v1
