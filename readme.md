# Streaming Learned ~~Bloom~~ Broom Filter

This is a python implementation of a streaming learned broom filter. This filter is
capable of remembering false positives and preventing an adversarial attack on a false positive key, while increasing the memory footprint by just 0.2%.

This code has the following components.

- A normal bloom filter
- A bloom filter bootstrapped with a neural engine, which is the broom filter.
- A consumer which pulls data from Kafka
- A producer which pushes data to Kafka
- A script which carries out an adversarial attack
- And a simple way to run all of it!

**Watch the tutorial here**: [Learned Broom Filter Tutorial](https://youtu.be/Yobja5S2dpY)

## Tech Stack Used

- Kafka
- Python (Flask)
- MongoDb
- Docker

## Disclaimer

This system is designed to run in docker end-to-end. However, we **strongly** recommend
that you run it on a system which has at least 32GB of RAM. We have observed the docker containers
crash in systems with low memory. Free of cost high performance cloud VMs can be found [here](https://www.cloudlab.us).

## How To Use

To launch the system, simply execute the following command:

```
docker-compose up --build
```

This command initializes Docker Compose, which orchestrates the setup and starts all the necessary services.

1. **Zookeeper**: Initializes first as it manages the configuration information and synchronization for Kafka.
2. **Kafka**: To handle streaming data.
3. **MongoDB**: Activates database services for storing and managing data.
4. **Python Server**: Finally, the Flask-based Python server launched which handles all the api requests.

For easy testing of the bloom filter, we created an automation shell script named `master_script.sh`. This script sequentially triggers the necessary operations to test both the learned broom filter and the traditional bloom filter, gather data, and generate a report.

To run the automation script, follow these instructions:

1. Navigate to the `shell` directory where the `master_script.sh` script is located. You can do this by executing the command:

   ```
   cd shell
   ```

2. You can run it with:
   ```
   ./master_script.sh
   ```

Make sure all related services (like your Flask server and Kafka) are up and running before executing the script to ensure it functions correctly.

The shell script does the following, the producer and consumer will be brought up, and this will pump data into the system. We have configured the system to only run with 1000 records. This is a small number, because for bigger workloads, the time taken for the test can range from a few minutes to an hour. Once all the data is pushed, the attacker script kicks in. Once the attack is finished, we report the maximum number of query for a false positive key from both the learned broom filter and a regular bloom filter, along with memory usage in the format `[neural_network_memory, bit_array_memory]`.

## Api Documentation

Here's the API documentation for the five endpoints described in your code, which correspond to various functionalities related to the bloom and learned broom filters:

### API Documentation

#### 1. Consume Kafka Messages

**Endpoint**: `GET /consume`
**Description**: Starts a consumer that subscribes to a specified Kafka topic and processes incoming messages. It continuously polls messages, inserts relevant keys into the bloom filter, and stores data in MongoDB until a stop signal is received or the partition end is reached.

#### 2. Produce Kafka Messages

**Endpoint**: `GET /produce/<dist>/<limit>`
**Parameters**:

- `dist` (string): Specifies the distribution type of user IDs to generate ('prime', 'mix', or 'random').
- `limit` (integer): The total number of messages to send to the Kafka topic.
  **Description**: Initiates the production of Kafka messages based on the specified distribution of user IDs. The data generated includes user activities with various attributes like product ID, timestamp, and price.

#### 3. Attack Learned Broom Filter

**Endpoint**: `GET /attack/<limit>`
**Parameters**:

- `limit` (integer): The maximum number of attempts to find a false positive key.
  **Description**: Performs an adversarial attack on the learned broom filter by continuously querying until a false positive key is found or the limit is reached.

#### 4. Attack Normal Bloom Filter

**Endpoint**: `GET /attack-normal/<limit>`
**Parameters**:

- `limit` (integer): The maximum number of attempts to find a false positive key in the normal bloom filter.
  **Description**: Similar to the attack on the learned broom filter, this endpoint targets the normal bloom filter to measure its susceptibility to false positives under the same conditions.

#### 5. Generate Report

**Endpoint**: `GET /report`
**Description**: Compiles and returns a report on the performance of both the learned broom filter and the normal bloom filter. It includes statistics like the maximum number of attempts needed to find a false positive and memory usage.
**Response**:

- Returns a JSON object with detailed statistics including maximum false positive attempts for both filters and current memory usage.
  ```json
  {
      "learned_filter": <number of attempts at a false positive key>,
      "bloom_filter": <number of attempts at a false positive key>,
      "memory_usage": [<memory usage in bytes>]
  }
  ```

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

- learned_filter: 5. This means that the learned broom filter took only 5 attempts at a false positive key to learn that this key was a false positive and block future requests. This is great, because a normal bloom filter will never block the requests.
- bloom_filter: 0. This does not mean that the bloom filter took 0 attempts to block false positive keys. The bloom filter has no blocking mechanism. This means that the normal bloom filter had no false positives at all. This has been mentioned in the report as well, and this is due to the efficacy of the hash functions when compared to a neural network, for our data.
- memory_usage: [56, 19170176]. This means that the neural network took 56B of memory, compared to the overall size of 19170176B. This is just a 0.2% increase.

## Conclusion

Our results show that the learned broom filter takes on average 5-7 attempts to learn that a key is false positive. This is much better than a normal bloom filter, where this value would be infinity. Of course, the neural network can be improved, and these details are present on the report.
