#!/bin/sh

workon domino

pip install -U -r ./app/requirements.txt
pip install ipython['notebook']

nohup ipython notebook &
docker-compose exec as /opt/anaconda/anaconda_server/docker/start python 19360 docker_project
