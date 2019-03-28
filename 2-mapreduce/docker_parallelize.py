import docker
import os
import math
import json
import collections
import tarfile
import time
import json
from io import BytesIO
from io import StringIO

CONTAINER_NAME = 'analysis_test'
DATA_DIRECTORY = os.path.abspath('data')
ANALYZE_DIRECTORY = os.path.abspath('docker_analyze.py')
N = 6

"""
Supervisor script to launch Docker containers and reduce the results produced by them.
"""

client = docker.Client()

def get_files(directory):
    filenames = os.listdir(directory)
    return sorted([filename for filename in filenames if filename.endswith('.json.gz')])

def reduce_output_files():
    filenames = [filename for filename in os.listdir(OUTPUT_DIRECTORY) if filename.endswith('.json')]
    results = []
    for filename in filenames:
        with open(os.path.join(OUTPUT_DIRECTORY,filename),'r') as input_file:
            results.append(json.loads(input_file.read()))
    return reduce_results(results)

def reduce_results(results):
    word_frequencies = collections.defaultdict(lambda:0)
    for result in results:
        for word, frequency in result.items():
            word_frequencies[word]+=frequency
    return word_frequencies  

# Copy over scripts to instances.
def save_file(filename, data, path, id):
    pw_tarstream = BytesIO()
    pw_tar = tarfile.TarFile(fileobj=pw_tarstream, mode='w')
    tarinfo = tarfile.TarInfo(name=filename)
    tarinfo.size = len(data)
    tarinfo.mtime = time.time()
    pw_tar.addfile(tarinfo, BytesIO(data))
    pw_tar.close()

    pw_tarstream.seek(0)
    client.put_archive(
        container=id,
        path=path, 
        data=pw_tarstream)

# Copy over data to instances.
def save_data(id):
    pw_tarstream = BytesIO()
    pw_tar = tarfile.TarFile(fileobj=pw_tarstream, mode='w')
    for filename in os.listdir(DATA_DIRECTORY):
        tarinfo = tarfile.TarInfo(name=filename)
        data = open(DATA_DIRECTORY + "/" +filename, 'r').read()
        tarinfo.size = len(data)
        tarinfo.mtime = time.time()
        pw_tar.addfile(tarinfo, BytesIO(data))
    pw_tar.close()

    pw_tarstream.seek(0)
    client.put_archive(
        container=id,
        path=DATA_DIRECTORY+"/",
        data=pw_tarstream)


def analyze_files_in_container(files):
    print("Launching container for files {}".format(", ".join(files)))

    # Binding between relevant folders.
    host_config = client.create_host_config(
        binds = {
            DATA_DIRECTORY : {
                'bind' : '/data',
                'mode' : 'rw'
            }
        },
        )

    environment = {
            'INPUT_FILENAMES' : ';'.join(files)
        }

    # Launch container, running in background.
    container = client.create_container(
        image='python:2',
        user=os.getuid(),
        host_config=host_config,
        environment=environment, 
        tty=True, stdin_open=True)  
    client.start(container) 

    # Transfer information from this container to instance.
    save_file("docker_analyze.py", open('docker_analyze.py', 'r').read(), "/", container['Id'])
    save_data(container['Id'])

    return container

if __name__ == '__main__':

    files = get_files(DATA_DIRECTORY)
    chunk_size = int(math.ceil(len(files)/float(N)))
    containers = []

    # Split the work between nodes.
    for i in range(0,len(files),chunk_size):
        files_chunk = files[i:i+chunk_size]
        containers.append(analyze_files_in_container(files_chunk))

    print("Waiting for containers to finish...")

    results = []
    for container in containers:
        # Run the analyze script.
        ex = client.exec_create(
            container=container['Id'],
            cmd="bash -c 'python docker_analyze.py'"
        )

        # Record response.
        response = client.exec_start(ex)
        json_list = response.split(";;")
        for j in json_list:
            if j.isspace():
                continue
            results.append(json.loads(j))
        client.exec_inspect(ex)['ExitCode']

        # Exit the worker node.
        try:
            exit_code = client.wait(container, timeout = 1)
            print("Container exited with code {}".format(exit_code))
        except:
            print("Container {} exited.".format(container['Id']))

    reduced_results = reduce_results(results)
    print("Top 100 words used in Github commits:")
    print("\n".join(["{:<40}:{}".format(word,frequency)
                     for word,frequency in 
                     sorted(reduced_results.items(),key=lambda x:-x[1])[:100]]))
