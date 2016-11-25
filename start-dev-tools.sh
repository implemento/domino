#!/bin/sh

nohup ipython notebook &
docker-compose exec as /opt/anaconda/anaconda_server/docker/start python 19360 docker_project
