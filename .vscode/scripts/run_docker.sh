#!/bin/sh

DockerContainerName="THD_Postgres"

# Check if Docker Compose is installed
if ! command -v docker-compose >/dev/null 2>&1
then
    echo "Docker Compose could not be found. Please install it first."
    exit 1
fi

# Check if Docker Compose is running
if ! docker-compose ps | grep 'Up' >/dev/null 2>&1
then
    echo "Docker Compose is not running. Building and starting..."
    docker-compose up --build -d Postgres
    # init variable
    numOfDBstartups=0

    # loop until SQL engine perform 2 complete startups, 
    # each startup is announced by log message "database system is ready to accept connections"
    # after first one Database is initialized from scripts located in "SQL" directory, 
    # once DB init is completed, another restart is performed and container is ready to work.
    while [ "$numOfDBstartups" -lt 1 ]; do
        
        sleep 0.1
        # check if container is still running, 
        #   if not display container logs.
        #   if yes invoke DB tests.

        # if there were some error during initialization container will not be running
        if [ -z "$(docker ps -q -f name="$DockerContainerName")" ]; then
        docker logs $DockerContainerName

        printRedMessage "Container is not running"
        exit 3
        fi
        numOfDBstartups=$(docker logs $DockerContainerName 2>&1 | grep -c "database system is ready to accept connections$")
    done
else
    echo "Docker Compose is already running."
fi