#!/bin/bash
sudo apt update
sudo apt install default-jdk
wget https://downloads.apache.org/kafka/3.7.0/kafka-3.7.0-src.tgz
tar -xzf kafka-3.7.0-src.tgz
sudo mv kafka-3.7.0-src /opt/kafka
export PATH=$PATH:/opt/kafka/bin
export JAVA_HOME=/usr/lib/jvm/default-java
chmod +x /opt/kafka/gradlew
cd /opt/kafka
./gradlew jar -PscalaVersion=2.13.12
zookeeper-server-start.sh -daemon /opt/kafka/config/zookeeper.properties
kafka-server-start.sh -daemon /opt/kafka/config/server.properties
cd ~