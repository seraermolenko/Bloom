#!/bin/zsh

kafka-topics --create \
  --bootstrap-server localhost:9092 \
  --topic water \
  --partitions 1 \
  --replication-factor 1

echo "Created topic: water"
