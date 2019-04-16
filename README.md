# Docker Tutorial
## CS308

## An Introduction to Docker
Have you ever wanted to:

1. Run code locally without installing tons of packages and dependencies on your computer?
2. Send code to a friend with a different computer and know it will run without failures?
3. Define a complicated set of configuration rules _just once_, rather than configuring a piece of software each time it runs?

These are all common problems that can be solved using _containerization_, which lets us package software into standardized units for development, shipment and deployment. The most commonly used tool for containerization is [Docker](https://www.docker.com/), which is:
> an open-source project that automates the deployment of software 
> applications inside containers by providing an additional layer 
> of abstraction and automation of OS-level virtualization on Linux.

This is a fancy way of saying that Docker provides a sandbox type of environment for deployment of applications, in the form of a Docker _container_. A container can be standardized and shipped out to many different machines are once, requiring little or no set-up to organize once the Docker framework is laid out. Docker is used by a variety of companies to:
* Increase developer productivity
* Release software at a faster rate
* Reduce the need for IT infrastructure
* Speed up deployment

## Installing Docker
Let's first install Docker. Download an installer for [Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac), [Linux](https://www.linux.com/learn/intro-to-linux/2017/11/how-install-and-use-docker-linux), or [Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows). You may have to create a Docker account to do so. Notes: 

* If you have a Linux computer, the installation of Docker is a bit more involved. If you are up for it, give it a try. Otherwise, try working with someone who has Docker installed.
* If you have a Windows computer, you must have Windows 10 Pro or Enterprise installed to download Docker this way.

Once the installation is complete, make sure that Docker is installed on your command line by running the following command:

	docker run hello-world
	> Hello from Docker....

If your output is as expected: Congrats! You officially have Docker installed. Otherwise, try one of the following solutions:
* Uninstalling and reinstalling Docker, potentially using commandline tools instead ([Stack Overflow](https://stackoverflow.com/questions/32744780/install-docker-toolbox-on-a-mac-via-command-line) can be very helpful with this). This can be done using tools like Homebrew (a package manager for Linux and Mac). 
* If the installation indicates that your Mac or Windows version is not high enough, try the alternate solution explained [here](https://docs.docker.com/toolbox/toolbox_install_windows/).
* If it seems to be a permission issue, run Docker as an administrator (e.g., on Mac, use `sudo`).

#
#
> ```diff
> + Checkpoint Number 1: At this point, you should have Docker installed.
> ```
#
#

## Busybox
We will now learn more about Docker by running a pre-configured container called [Busybox](https://en.wikipedia.org/wiki/BusyBox). Busybox provides several Unix utilities in a single source, giving us plenty of built-in functionality with which to work. To get started, fetch the busybox image from the Docker registry:

	docker pull busybox

By running this command, we retrieve a local version of Busybox to launch as a container on our system. We can now test this container by typing:

	docker run busybox echo "I love Busybox"

By passing a command, we instruct the container to  launch, execute our command from within the Busybox container, and then exit. This all happens in a split second!

_So why run our command through a docker container? Isn't this just extra work?_ The answer to this question becomes more apparent as we advance to more complex applications. 

## Docker and Webapps 
We are now going to use Docker to deploy a static website. Navigate to the `1-static-webapp` directory in this tutorial repository and explore the files there. 

The `html` folder holds all of the static content to be served on the website (including HTML and CSS). The `Dockerfile` is of particular importance -- this file defines the base image for our Docker container. Because we are running a very simple application, the Dockerfile for this example is mainly composed of an installation of Nginx, a web server tool that lets us deploy HTML for a website.

To build our static HTML image (basically the blueprint for a docker container), run the following command:

	docker build -t webapp-image:v1 .

This command builds and configures a docker container. We can now launch this container by name by connecting host port 80 to container port 80 with the command:

	docker run -d -p 80:80 webapp-image:v1

Now follow the relevant instructions to view the static webpage:
* Mac/Linux: Visit the page `localhost:80` in your local browser.
* Windows: Run the command `docker-machine ip`and visit `<ip>:80` in your local browser.

If you do not see anything, try reading the next section and using the `1_docker_reset.sh` script to reset and run everything.

### Making Changes
Try following the instructions listed on the static webpage. Once you have made these changes in the `1-static-webapp` folder, run `docker ps -a` and find the docker container with the status 'Up.'  Run the following commands to get a fresh start by stopping and removing the old docker container:

	docker stop <container_id>

	docker rm <container_id>

After this, you can run the same commands as before to spin up your docker container. There are more efficient ways to do this, but we will stick with this for ease of understanding. Now you can rebuild and launch an entirely fresh container with your new changes. To do all of these tasks quickly, run the `1_docker_reset` script. Run this script from `1-static-webapp` with the command:

	./../util/1_docker_reset.sh

If you get a _Permission Denied_ error, try changing the permissions on the file by running one of the following commands from the `1-static-webapp` folder:

* Mac/Linux: `chmod +x ../util/1_docker_reset.sh`
* Windows: `cacls ../util/1_docker_reset.sh /g everyone:f`

#
#
> ```diff
> + Checkpoint Number 2: At this point, you should have a modified webpage running locally.
> ```
#
#

### Why does this help us?
To see the difference between your local computer and the container, run the following commands:

	docker run webapp-image:v1 nginx -v

	nginx -v

Unless you already had nginx installed on your computer, you should observe that the first command prints out a nginx version while the latter does not. This is because all of the configuration was accomplished on the docker container, rather than your local computer. When you kill this container, the configuration will go with it. With more advanced webpages, we may need a variety of resources to be installed on the container. Docker handles all of this configuration without modifying your local computer settings.

## Docker and MapReduce

### MapReduce

In this example, we will incorporate MapReduce. MapReduce is a programming paradigm that enables massive scalability across up to thousands of servers in a cluster. This paradigm performs two types of tasks: (1) Map: Performs sorting and filtering, (2) Reduce: Performs summary operations. This lets us parallize work (e.g., data analysis). Learn more about MapReduce in this [tutorial](https://hadoop.apache.org/docs/r1.2.1/mapred_tutorial.html).

### Example
Navigate to the `2-mapreduce` folder. This is a very simple example of realizing a map-reduce style workflow with Docker and Python. Note that this example is inspired by the tutorial in this [project](https://github.com/adewes/docker-map-reduce-example/blob/master/README.md).

Examine the data in the `data` folder. These JSON files represent commit data for several days from Github. If you want fresh data, you must have `wget` installed. Try typing the following to determine if you have `wget`:
	
	which wget
	
If you do not have `wget` already installed, this step is optional. If you would like to install `wget` and pull the data, you can do so by visting the following links:
* Mac/Linux: Installation [here](https://www.cyberciti.biz/faq/howto-install-wget-om-mac-os-x-mountain-lion-mavericks-snow-leopard/)
* Windows: Installation [here](http://gnuwin32.sourceforge.net/packages/wget.htm)
	
Data can then be retrieved by running:

	./fetch_data.sh


#### Normal Analysis

To analyze the data normally (with no Docker), we use Python on our local computer. If you already have Python installed, proceed with this example. If you would like to install it, explore how to do this using this [site](https://www.python.org/downloads/release/python-2715/
). Make sure to download Version 2.7 for consistency. With Python installed, we can run the analysis script locally:

	python analyze.py      # optional

This script runs through days of commit messages and tallies how many instances of each word there are. It then spits out the top 100 words used in commit messages. This type of task can be split into sub-tasks (analyzing chunks of time) run via Docker. The output looks something like this:
```
Top 100 words used in Github commits:
node_modules                            :95254
to                                      :46432
the                                     :43311
-                                       :40486
a                                       :26657
for                                     :25784
...
an                                      :3270
apis                                    :3248
index                                   :3244
```

#### Dockerized Analysis

For the Docker-based version of this example, you do _not_ need to install Python. This is the beauty of Docker -- we can run the entire script in a Docker container without modifying our local computer.

Take a minute to examine the Dockerfile for this example. It is much more complex than the previous Dockerfile. You will see that both the `docker_parallelize.py` and `docker_analyze.py` scripts are copied into the container, as we will be executing the parallelize script from the master container, and the analyze script from the subsequent slave containers. You will also note that Python is installed within the Docker container to run these scripts. 

To build the Docker image required for the docker-based analyis, run:

    docker build -t mapreduce-image:v1 .

We can then run the master Docker container. Because we will be launching a series of additional Docker containers from the master container, we need to have Docker also running here. This is why we pass in the `/var/run.docker.sock` variable for our container. 

    docker run -v /var/run/docker.sock:/var/run/docker.sock mapreduce-image:v1

This is simplified in the `2_docker_reset.sh` script in the util folder, which removes old docker containers and runs the `docker_parallelize.py` script. Note that it does not handle data fetching.

The steps described prior will launch a number of Docker containers, each of which will analyze a portion of the data using the `docker_analyze.py` script. This lets us parallelize the work across several workers, which can be launched on separate machines. We still see the same output from this script as the normal data analysis because the results are aggregated at the end of the process. You should see the same output from this series of steps as the "normal" analysis. *This will take a couple of minutes, so be patient.* 

#
#
> ```diff
> + Checkpoint Number 3: At this point, you should have a valid output from the Dockerized script.
> ```
#
#

## Conclusion
In this tutorial, you have learned the basics of the tool _Docker_. As you will learn in later tutorials, Docker is revolutionary in the world of cloud computing. Docker lets us launch the exact same code, with the exact same configurations, across thousands of worker nodes in the cloud. This lets us run computationally complex tasks in no time at all. Companies that use Docker to handle massive amounts of data and analysis include:
* PayPal
* Spotify
* Ebay
* Groupon
* Uber

Larger companies like Google and Facebook have internal equivalents. 

Explore how Docker can help with cloud computing in the [next tutorial, focusing on AWS.](https://github.com/JamesDaubert/aws-server-tutorial)


#
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
* https://gist.github.com/zbyte64/6
0eae10ce082bb78f0b7a2cca5cbc2
