#!/bin/bash

# Wait for Kafka to be ready
sleep 30

# Create Kafka topics
kafka-topics --bootstrap-server kafka:9092 --topic first_topic --create --partitions 1 --replication-factor 1
