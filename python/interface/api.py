"""
@author Aaditya
@version 0.1
@since 17-03-2024
This file contains the public API for the learned bloom filter. It can be used standalone or as part of the
larger test module.
FOR EXTERNAL USE
"""
<<<<<<< HEAD
=======
import sys
import os

# Add the parent directory of 'Filter' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import jsonify
>>>>>>> master
from confluent_kafka import KafkaError

from Filter import BloomFilter
from enum import Enum
import json
<<<<<<< HEAD
=======
import pymongo
>>>>>>> master


class MODE(Enum):
    REST = 0
    STREAM = 1
<<<<<<< HEAD
=======
    DEBUG = 2
>>>>>>> master


class LearnedBloomFilter:
    """
    Constructor: returns an instance of LearnedBloomFilter
    :param mode: possible values [stream, debug]
    In stream mode, we will require two additional arguments (optargs). Data will be read from a kafka stream
    In debug mode, this will function like a normal REST api.
    :param optargs: a list of strings, the first value is the address of the bootstrap server, second is kafka topic name
    """

<<<<<<< HEAD
    def __init__(self, mode, optargs):
        self.mode = mode
        self.filter = BloomFilter.create_filter_with_defaults()
=======
    def __init__(self, mode, optargs=None):
        self.mode = mode
        self.filter = BloomFilter.create_filter_with_defaults()
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db_name = "stream_db"
        self.db = self.client[self.db_name]
        self.collection_name = "producer_collection"
        self.collection = self.db[self.collection_name]
>>>>>>> master
        if mode == MODE.STREAM:
            self.optargs = optargs
            self.consumer = BloomFilter.create_filter_with_stream_config(self.filter, optargs)
        return

    def consume(self):
        self.consumer.subscribe([self.optargs[1]])
        while True:
            msg = self.consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition
                    break
                else:
                    # Error
                    print(msg.error())
                    break
            data = json.loads(msg.value().decode('utf-8'))
            key = msg.key()
            self.filter.insert(int(key))
<<<<<<< HEAD
            # TODO call to DB for insert
=======
            self.collection.insert_one(data)
>>>>>>> master

    """
    Only to be used in REST mode
    """

    def insert(self, key):
<<<<<<< HEAD
        if self.mode != MODE.REST:
            raise ValueError("Invalid mode. Expected MODE.REST.")
        self.filter.insert(key)
=======
        self.filter.insert(key)
        doc = {'key': key}
        self.collection.insert_one(doc)
>>>>>>> master
        return

    """
    Only to be used in REST mode
    """

    def query(self, key):
<<<<<<< HEAD
        if self.mode != MODE.REST:
            raise ValueError("Invalid mode. Expected MODE.REST.")
        return self.filter.query(key)
=======
        found = False
        result = self.filter.query_nn(key)
        if result:
            collection = self.collection.find_one({'key': key})
            if collection:
                found = True
        json_result = {
            "Present": result,
            "found_in_db": found
        }
        # retrain the nn here if found = false
        if not found:
            self.filter.train_one(key)
        return jsonify(json_result)
>>>>>>> master
