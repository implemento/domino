FROM debian:jessie

RUN apt-get update && \
    apt-get install -y \
      openvpn \
      ssh \
      vpnc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
