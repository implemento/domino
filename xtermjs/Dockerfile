FROM node:6.8.0

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ARG NODE_ENV
ENV NODE_ENV $NODE_ENV

COPY etc/apt/sources.list.d/docker.list /etc/apt/sources.list.d/docker.list

RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 \
            --recv-keys 58118E89F3A912897C070ADBF76221572C52609D && \
    apt-get update && \
    apt-get install -y docker-engine vim && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    git clone https://github.com/sourcelair/xterm.js . && \
    npm install

EXPOSE 3000
