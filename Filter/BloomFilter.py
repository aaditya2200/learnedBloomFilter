from array import array
import math
import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding, Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from tensorflow.keras.models import Model
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
        # self.model = tf.keras.Sequential([
        #     tf.keras.layers.Dense(64, activation='relu', input_shape=(64,)),
        #     tf.keras.layers.Dense(32, activation='relu'),
        #     tf.keras.layers.Dense(units=16, activation='relu'),
        #     tf.keras.layers.Dense(1, activation='sigmoid')
        # ])
        input_size = 64  # Assuming 64-bit input representation
        embedding_size = 32  # Embedding size for input bits
        conv_layers = [[64, 4, 2], [32, 3, 2]]  # Convolutional layers: [filters, kernel_size, pooling_size]
        fully_connected_layers = [32, 1]  # Fully connected layers
        dropout_p = 0.5  # Dropout probability
        optimizer = 'adam'
        loss = 'binary_crossentropy'

        # Define the input layer
        inputs = Input(shape=(input_size,), name='input', dtype='int64')

        # Embedding layer
        embedding_layer = Embedding(input_dim=2, output_dim=embedding_size, input_length=input_size)
        embedded_inputs = embedding_layer(inputs)

        # Convolutional layers
        x = embedded_inputs
        for filters, kernel_size, pooling_size in conv_layers:
            x = Conv1D(filters=filters, kernel_size=kernel_size, activation='relu')(x)
            x = MaxPooling1D(pool_size=pooling_size)(x)

        # Flatten the output
        x = Flatten()(x)

        # Fully connected layers
        for units in fully_connected_layers:
            x = Dense(units, activation='relu')(x)
            x = Dropout(dropout_p)(x)

        # Output layer
        predictions = Dense(1, activation='sigmoid')(x)

        # Build the model
        self.model = Model(inputs=inputs, outputs=predictions)
        self.model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    def insert(self, key):
        for func in self.hash_func_list:
            index = int(func(key) % self.number_of_bits)
            self.bloom[index] = 1
        # Now, lets train our model also.

        X_train, y_train = np.array([integer_to_binary(key)]), np.array([[1]])
        self.model.train_on_batch(X_train, y_train)

    def train(self, nums):
        for item in nums:
            X_train, y_train = np.array([integer_to_binary(item)]), np.array([[0]])
            self.model.train_on_batch(X_train, y_train)

    def query(self, key):
        for func in self.hash_func_list:
            index = int(func(key) % self.number_of_bits)
            if self.bloom[index] != 1:
                return False
        return True

    def query_nn(self, key):
        prediction = self.model.predict(np.array([integer_to_binary(key)]))
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
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(bf.kafka_cfg)
    return consumer
