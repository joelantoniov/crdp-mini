#! /bin/sh
sudo docker exec -it kafka-broker bash -c "/usr/bin/kafka-topics --list --bootstrap-server localhost:9092"
