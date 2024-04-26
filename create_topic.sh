#!/bin/bash
# create-topics.sh

# Kafka waits for Zookeeper to be ready before starting
# wait for Kafka to be up
kafka-topics.sh --bootstrap-server localhost:9092 --list

# create the ecommerce_activity topic
kafka-topics.sh --bootstrap-server localhost:9092 --topic ecommerce_activity --create --if-not-exists --partitions 1 --replication-factor 1
