# Streaming Learned ~~Bloom~~ Broom Filter

This is a python implementation of a streaming learned broom filter. This filter is
capable of remembering false positives and preventing an adversarial attack on a false positive key, while increasing the memory 
footprint by just 0.2%. This code has the following components.
- A normal bloom filter
- A bloom filter bootstrapped with a neural engine, which is the broom filter.
- A consumer which pulls data from Kafka
- A producer which pushes data to Kafka
- A script which carries out an adversarial attack
- And a simple way to run all of it!


## Tech Stack Used

- Kafka
- Python
- MongoDb
- Docker

## Disclaimer
This system is designed to run in docker end-to-end. However, we **strongly** recommend 
that you run it on a system which has at least 32GiB of RAM. We have observed the docker containers
crash in systems with low memory. Free of cost high performance cloud VMs can be found [here](https://www.cloudlab.us).

## How To Use
All you have to do is run ```docker compose up --build```. Docker will then bring up Zookeper, Kafka, MongoDB, and then start the python
server. After this, the producer and consumer will be brought up, and this will pump data into the system. We have configured
the system to only run with 1000 records. This is a small number, because for bigger workloads, the time taken for the test can
range from a few minutes to an hour. Once all the data is pushed, the attacker script kicks in. Once the attack is finished,
we report the maximum number of query for a false positive key from both the learned broom filter and a regular bloom filter, along with memory usage
in the format ```[neural_network_memory, bit_array_memory]```.