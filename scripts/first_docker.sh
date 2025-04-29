#!/bin/bash
sudo docker run -d \
  --name zookeeper \
  --network crdp-cassandra-net \
  -e ZOOKEEPER_CLIENT_PORT=2181 \
  -p 2181:2181 \
  zookeeper:latest
