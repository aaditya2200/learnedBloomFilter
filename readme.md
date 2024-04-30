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

## How To Interpret Results
You will receive results in the following format. 
```
{
    "bloom_filter": 0,
    "learned_filter": 5,
    "memory_usage": [
        56,
        19170196
    ]
}
```

The numbers can be interpreted as follows:
- learned_filter: 5. This means that the learned broom filter took only 5 attempts at a false positive key to learn that this key was a false positive and block future requests. This is great, because a normal bloom filter
  will never block the requests.
- bloom_filter: 0. This does not mean that the bloom filter took 0 attempts to block false positive keys. The bloom filter has no blocking mechanism. This means that the normal bloom filter had no false positives at all. This has been mentioned in the report as well, and this is due to the efficacy of the hash functions when compared to a neural network, for our data.
- memory_usage: [56, 19170176]. This means that the neural network took 56B of memory, compared to the overall size of 19170176B. This is just a 0.2% increase.

## Conclusion
Our results show that the learned broom filter takes on average 5-7 attempts to learn that a key is false positive. This is much better than a normal bloom filter, where this value would be infinity. Of course, the neural network can be improved, and these details are present on the report.  
