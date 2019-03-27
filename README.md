# Docker Tutorial
## CS308

## An Introduction to Docker
Have you ever wanted to:

1. Run code locally without installing tons of packages and dependencies on your computer?
2. Send code to a friend with a different computer and know it will run without failures?
3. Define a complicated set of configuration rules _just once_, rather than configuring a piece of software each time it runs?

These are all common problems and scenarios that can be solved using _containerization_, which lets us package software into standardized units for development, shipment and deployment. The most commonly used tool for containerization is [Docker](https://www.docker.com/).

Docker is:
> an open-source project that automates the deployment of software 
> applications inside containers by providing an additional layer 
> of abstraction and automation of OS-level virtualization on Linux.

This is a fancy way of saying that Docker provides a sandbox type of environment for deployment of applications, in the form of a Docker _container_. A container can be standardized and shipped out to many different machines are once, requiring little or no set-up to organize once the Docker framework is laid out. Docker is used by a variety of companies to:
* Increase developer productivity
* Release software at a faster rate
* Reduce the need for IT infrastructure
* Speed up deployment

## Getting Started with Docker
Let's first install Docker. Download an installer for [Mac](https://www.docker.com/products/docker-engine#/mac), [Linux](https://www.docker.com/products/docker-engine#/linux), or [Windows](https://www.docker.com/products/docker-engine#/windows). Once the installation is complete, make sure that Docker is installed on your command line by running the following command:

`docker run hello-world`

`> Hello from Docker....`

Congrats! You officially have Docker installed.

## Busybox
We will now learn more about Docker by running a [Busybox](https://en.wikipedia.org/wiki/BusyBox) container. Busybox provides several Unix utilities in a single source, giving us plenty of built-in functionality with which to work. To get started, fetch the busybox image from the Docker registry:

`docker pull busybox`

By running this command, we retrieve a local version of Busybox to launch as a container on our system. We can now test this container by typing:

`docker run busybox echo "I love Busybox!"`

By passing a command, we instruct the container to  launch, execute our command, from within the Busybox container and then exit. This all happens in a split second!

_So why run our command through a docker container? Isn't this just extra work?_ The answer to this question becomes more apparent as we advance to more complex applications. 

## Docker and Webapps 
We are now going to use Docker to deploy a static website. Navigate to the `1-static-webapp` directory in this tutorial repository and explore the files there. 

The `html` folder holds all of the static content to be served on the website (including HTML). The `Dockerfile` is of particular importance -- this file defines the base image for our Docker container. Because we are running a very simple application, the Dockerfile for this example is mainly composed of installation of Nginx, a web server tool that lets us deploy HTML for a website.

To build our static HTML image, run the following command:

`docker build -t webapp-image:v1 .`

This command builds and configures a docker container. We can now launch this container on host port and container port 80 with the command:

`docker run -d -p 80:80 webapp-image:v1`

If you visit the page localhost:80, you should now see the static webpage! 

### Making Changes
Try following the instructions listed on the static webpage. Once you have made these changes in the `1-static-webapp` folder, run `docker ps -a` and find the docker container with the status 'Up.'  Run the following commands to get a fresh start:

`docker stop <container_id>`

`docker rm <container_id>`

There are more efficient ways to do this, but we will stick with this for ease of understanding. Now you can rebuild and launch an entirely fresh container with your new changes. To do all of these tasks quickly, run the `1_docker_reset` script. You can either run this script from `1-static-webapp` with the command:

`./../util/1_docker_reset.sh`

Or you can run this script by navigating to the `util` folder and run:

`./1_docker_reset.sh`

If you get a _Permission Denied_ error, try running the following command from the `util` folder:

`chmod +x 1_docker_reset.sh`

This command changes the permissions on the file so that you can run it locally.


### Why does this help us?
To see the difference between your local computer and the container, run the following commands:

`docker run webapp-image:v1 nginx -v`

`nginx -v`

Unless you already had nginx installed on your computer, you should observe that the first command prints out a nginx version while the latter does not. This is because all of the configuration was accomplished on the docker container, rather than your local computer. When you kill this container, the configuration will go with it. With more advanced webpages, we may need a variety of resources to be installed on the container. Docker handles all of this configuration without modifying your local computer settings.

## Docker and MapReduce

### MapReduce

In this example, we will incorporate MapReduce. MapReduce is a programming paradigm that enables massive scalability across up to thousands of servers in a cluster. This paradigm performs two types of tasks: (1) Map: Performs sorting and filtering, (2) Reduce: Performs summary operations. This lets us parallize work (e.g., data analysis). Learn more about MapReduce in this [tutorial](https://hadoop.apache.org/docs/r1.2.1/mapred_tutorial.html).

### Example
Navigate to the `2-mapreduce` folder. This is a very simple example of realizing a map-reduce style workflow with Docker and Python. Note that this example is inspired by the tutorial in this [project](https://github.com/adewes/docker-map-reduce-example/blob/master/README.md).

The example uses data from Github. To fetch the data, simply run:

	`fetch_data.sh`

The data now lives in the `data` folder, representing commit data for several days from Github.

To analyze the data normally (with no Docker):

    python analyze.py

This script runs through days of commit messages and tallies how many instances of each word there are. It then spits out the top 100 words used in commit messages. This type of task can be split into sub-tasks (analyzing chunks of time) run via Docker.

To build the Docker image required for the docker-based analyis, run

    docker build -t example-image:v1 .

Then simply run

    python docker_parallelize.py

This is simplified in the `docker_reset.sh` script in the util folder, which removes old docker containers. Note that it does not handle data fetching.

This will launch a number of Docker containers, each of which will analyze a portion of the data using the `docker_analyze.py` script. This lets us parallelize the work across several workers, which can be launched on separate machines. We still see the same output from this script as the normal data analysis because the results are aggregated at the end of the process.



## Useful Docker commands:

* `docker ps`: List all running containers.
* `docker ps -a`: List all containers.
* `docker rm <container ID>`: Delete docker container.
* `docker rm $(docker ps -a -q -f status=exited)`: Delete all exited containers.

## Terminology:
* Images - The blueprints of our application which form the basis of containers. In the demo above, we used the `docker pull` command to download the busybox image.
* Containers - Created from Docker images and run the actual application. We create a container using docker run which we did using the busybox image that we downloaded. A list of running containers can be seen using the `docker ps` command.
* Docker Daemon - The background service running on the host that manages building, running and distributing Docker containers. The daemon is the process that runs in the operating system to which clients talk to.
* Docker Client - The command line tool that allows the user to interact with the daemon. 
* Docker Hub - A registry of Docker images. You can think of the registry as a directory of all available Docker images. 

## Sources:

* https://docker-curriculum.com/
* https://www.katacoda.com/courses/docker/create-nginx-static-web-server
* https://github.com/prakhar1989/docker-curriculum/blob/master/static-site/html/index.html
* https://github.com/adewes/docker-map-reduce-example/blob/master/README.md
