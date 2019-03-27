FROM ubuntu:16.04
RUN apt-get update
RUN apt-get install -y python2.7
COPY docker_analyze.py /docker_analyze.py
CMD ["python2.7","/docker_analyze.py"]