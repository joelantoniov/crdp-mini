#!/bin/bash
for region in jakarta nyc london sydney saopaulo; do
  sudo docker exec -it kafka-broker bash -c "/usr/bin/kafka-topics --create \
    --bootstrap-server localhost:9092 \
    --replication-factor 1 \
    --partitions 2 \
    --topic crdp-sensors-${region}"
done
