from array import array
import math
import tensorflow as tf
import numpy as np
class BloomFilter:
    def __init__(self, num_hash_functions, num_entries, false_pos_rate, hash_func_list):
        self.num_hash_functions = num_hash_functions
        self.num_entries = num_entries
        self.false_pos_rate = false_pos_rate
        self.number_of_bits = int(-1 * (num_entries * math.log(false_pos_rate)) / pow(math.log(2.0), 2))
        self.hash_func_list = hash_func_list
        self.bloom = array('i', [0] * self.number_of_bits)
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(1,)),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    def insert(self, key):
        for func in self.hash_func_list:
            index = int(func(key) % self.number_of_bits)
            self.bloom[index] = 1
        # Now, lets train our model also.
        X_train, y_train = np.array([[key]]), np.array([[1]])
        self.model.train_on_batch(X_train, y_train)

    def query(self, key):
        for func in self.hash_func_list:
            index = int(func(key) % self.number_of_bits)
            if self.bloom[index] != 1:
                return False
        return True

    def query_nn(self, key):
        prediction = self.model.predict(np.array([[key]]))
        return (prediction > 0.5).astype(int)
