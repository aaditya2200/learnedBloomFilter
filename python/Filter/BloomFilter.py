"""
@author Aaditya
@version 0.1
@since 17-03-2024
Bloom filter internal code. DO NOT USE DIRECTLY. CONSUME ONLY VIA api.py
"""
from array import array
import math
import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding, Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from tensorflow.keras.models import Model
from keras import Sequential
from keras.src.layers import Dense
import numpy as np
from Hashes import hash
from kafka import KafkaConsumer
from confluent_kafka import Consumer, KafkaError


def integer_to_binary(id):
    return np.array([int(bit) for bit in bin(id)[2:].zfill(64)])


class BloomFilter:
    def __init__(self, num_hash_functions, num_entries, false_pos_rate, hash_func_list):
        self.kafka_cfg = None
        self.num_hash_functions = num_hash_functions
        self.num_entries = num_entries
        self.false_pos_rate = false_pos_rate
        self.number_of_bits = int(-1 * (num_entries * math.log(false_pos_rate)) / pow(math.log(2.0), 2))
        self.hash_func_list = hash_func_list
        self.bloom = array('i', [0] * self.number_of_bits)
        self.neural_network = model = Sequential([
            Dense(64, activation='relu', input_shape=(64,), name='input_layer'),
            Dense(32, activation='relu', name='hidden_layer'),
            Dense(1, activation='sigmoid', name='output_layer')
        ])
        self.optimizer = 'adam'
        self.loss = 'binary_crossentropy'
        self.neural_network.compile(self.optimizer, self.loss, metrics=['accuracy'])


    def insert(self, key):
        for func in self.hash_func_list:
            index = int(func(key) % self.number_of_bits)
            self.bloom[index] = 1
        # Now, lets train our model also.

        X_train, y_train = np.array([integer_to_binary(key)]), np.array([[1]])
        self.neural_network.train_on_batch(X_train, y_train)

    def train(self, nums):
        for item in nums:
            x_train, y_train = np.array([integer_to_binary(item)]), np.array([[0]])
            self.neural_network(x_train, y_train)

    def train_one(self, item):
        x_train, y_train = np.array([integer_to_binary(item)]), np.array([[0]])
        self.neural_network(x_train, y_train)

    def query(self, key):
        for func in self.hash_func_list:
            index = int(func(key) % self.number_of_bits)
            if self.bloom[index] != 1:
                return False
        return True

    def query_nn(self, key):
        prediction = self.neural_network.predict(np.array([integer_to_binary(key)]))
        if prediction > 0.9:
            return True
        else:
            return self.query(key)


def create_filter_with_defaults():
    bf = BloomFilter(4, 1000, 0.1, hash.Hash().get_default_hash_spec())
    return bf


def create_filter_with_stream_config(bf, optargs):
    bootstrap_server_name = optargs[0]
    topic_name = optargs[1]
    consumer = KafkaConsumer(topic_name, bootstrap_servers=[bootstrap_server_name])
    bf.kafka_cfg = {
        'bootstrap.servers': bootstrap_server_name,
        'auto.offset.reset': 'earliest',
        'group.id': 'test'
    }
    consumer = Consumer(bf.kafka_cfg)
    return consumer
