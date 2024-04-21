#!/bin/bash

kafka-topics.sh --create --topic stream-test --bootstrap-server localhost:9092
kafka-console-producer.sh --topic tstream-test --bootstrap-server localhost:9092
kafka-console-consumer.sh --topic stream-test --bootstrap-server localhost:9092 --from-beginning
