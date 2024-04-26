"""
@author Aaditya and Sam Blesswin
@version 0.1
@since 17-03-2024
This file contains the public API for the learned bloom filter. It can be used standalone or as part of the
larger test module.
FOR EXTERNAL USE
"""

import sys
import os

# Add the parent directory of 'Filter' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from flask import jsonify
from confluent_kafka import KafkaError

from Filter import BloomFilter
from enum import Enum
import json
import pymongo


class MODE(Enum):
    REST = 0
    STREAM = 1
    DEBUG = 2


class LearnedBloomFilter:
    """
    Constructor: returns an instance of LearnedBloomFilter
    :param mode: possible values [stream, debug]
    In stream mode, we will require two additional arguments (optargs). Data will be read from a kafka stream
    In debug mode, this will function like a normal REST api.
    :param optargs: a list of strings, the first value is the address of the bootstrap server, second is kafka topic name
    """

    def __init__(self, mode, optargs=None):
        self.mode = mode
        self.filter = BloomFilter.create_filter_with_defaults()
        self.client = pymongo.MongoClient("mongodb://mongodb:27017/")
        self.db_name = "stream_db"
        self.db = self.client[self.db_name]
        self.collection_name = "producer_collection"
        self.collection = self.db[self.collection_name]
        if mode == MODE.STREAM:
            self.optargs = optargs
            self.consumer = BloomFilter.create_filter_with_stream_config(
                self.filter, optargs
            )
        return

    def consume(self):
        try:
            self.consumer.subscribe([self.optargs[1]])  # subscribe to kafka topic
            while True:
                msg = self.consumer.poll(
                    1.0
                )  # Poll for messages with a timeout of 1 second
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition, consumer has reached the end
                        break
                    else:
                        # Error
                        print(msg.error())
                        break
                data = json.loads(msg.value().decode("utf-8"))
                key = msg.key()

                if key == -1:
                    explicit_stop = True  # Producer signaled stop
                    break

                self.filter.insert(int(key))  # insert the key into the filter
                self.collection.insert_one(data)  # insert data into mongodb collection
            return True, "explicit stop" if explicit_stop else "partition eof"
        except Exception as e:
            print(f"An error occurred: {e}")
            return False, "exception"  # Return False if an exception occurs

    """
    Only to be used in REST mode
    """

    def insert(self, key):
        self.filter.insert(key)
        doc = {"key": key}
        self.collection.insert_one(doc)
        return

    """
    Only to be used in REST mode
    """

    def query(self, key):
        found = False
        result = self.filter.query_nn(key)  # filter the query for key
        if result:
            collection = self.collection.find_one({"key": key})
            if collection:
                found = True
        json_result = {"Present": result, "found_in_db": found}
        # retrain the nn here if found = false
        if result and not found:
            self.filter.train_one(key)
        return jsonify(json_result)
