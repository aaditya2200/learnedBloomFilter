"""
@author Aaditya
@version 0.1
@since 17-03-2024
This file contains the public API for the learned bloom filter. It can be used standalone or as part of the
larger test module.
FOR EXTERNAL USE
"""
from confluent_kafka import KafkaError

from Filter import BloomFilter
from enum import Enum
import json


class MODE(Enum):
    REST = 0
    STREAM = 1


class LearnedBloomFilter:
    """
    Constructor: returns an instance of LearnedBloomFilter
    :param mode: possible values [stream, debug]
    In stream mode, we will require two additional arguments (optargs). Data will be read from a kafka stream
    In debug mode, this will function like a normal REST api.
    :param optargs: a list of strings, the first value is the address of the bootstrap server, second is kafka topic name
    """

    def __init__(self, mode, optargs):
        self.mode = mode
        self.filter = BloomFilter.create_filter_with_defaults()
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
            # TODO call to DB for insert

    """
    Only to be used in REST mode
    """

    def insert(self, key):
        if self.mode != MODE.REST:
            raise ValueError("Invalid mode. Expected MODE.REST.")
        self.filter.insert(key)
        return

    """
    Only to be used in REST mode
    """

    def query(self, key):
        if self.mode != MODE.REST:
            raise ValueError("Invalid mode. Expected MODE.REST.")
        return self.filter.query(key)
