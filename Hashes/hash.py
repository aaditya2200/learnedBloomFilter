"""
This file contains all hash functions
"""


class Hash:
    def __init__(self):
        return
    def division_hash(self, key):
        return key % 997

    def multiplication_hash(self, key):
        return (key * 2654435761) & 0xFFFFFFFF

    def bitwise_xor_hash(self, key):
        return key ^ (key >> 16)

    def sax_hash(self, key):
        key = (~key) + (key << 21)  # key = (key << 21) - key - 1;
        key = key ^ (key >> 24)
        key = (key + (key << 3)) + (key << 8)  # key * 265
        key = key ^ (key >> 14)
        key = (key + (key << 2)) + (key << 4)  # key * 21
        key = key ^ (key >> 28)
        key = key + (key << 31)
        return key

    def get_default_hash_spec(self):
        return [self.division_hash, self.sax_hash, self.multiplication_hash, self.bitwise_xor_hash]