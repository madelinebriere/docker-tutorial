FROM ubuntu:16.04
FROM python:2
RUN apt-get update
RUN apt-get install -y python2.7
RUN apt-get install -y python-pip
RUN pip install docker-py
ADD data /data
ADD data/* /data/
COPY docker_parallelize.py /docker_parallelize.py
COPY docker_analyze.py /docker_analyze.py
COPY run.sh /run.sh
CMD ["python2.7","-u", "/docker_parallelize.py"]