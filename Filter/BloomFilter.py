from bitarray import bitarray
from array import array
import math


class BloomFilter:
    def __init__(self, num_hash_functions, num_entries, false_pos_rate, hash_func_list):
        self.num_hash_functions = num_hash_functions
        self.num_entries = num_entries
        self.false_pos_rate = false_pos_rate
        self.number_of_bits = int(-1 * (num_entries * math.log(false_pos_rate)) / pow(math.log(2.0), 2))
        self.hash_func_list = hash_func_list
        self.bloom = array('i', [0] * self.number_of_bits)

    def insert(self, key):
        for func in self.hash_func_list:
            index = int(func(key) % self.number_of_bits)
            self.bloom[index] = 1

    def query(self, key):
        for func in self.hash_func_list:
            index = int(func(key) % self.number_of_bits)
            if self.bloom[index] != 1:
                return False
        return True
