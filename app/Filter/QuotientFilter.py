"""
@author Aaditya and Sam Blesswin
@version 0.1
@since 17-03-2024
NOT TO BE USED, STILL IN DEV
"""
import math

class QuotientFilter:
    @staticmethod
    def calculate_bytes(q, r):
        bits = (1 << q) * (r + 3)
        bytes = bits // 8
        if bits % 8 != 0:
            bytes += 1
        return bytes

    def __init__(self, num_hash_functions, num_entries, false_pos_rate, hash_func, q, r):
        self.num_hash_functions = num_hash_functions
        self.num_entries = num_entries
        self.false_pos_rate = false_pos_rate
        self.number_of_bytes = QuotientFilter.calculate_bytes(q, r)
        self.hash_func = hash_func
        self.q = q
        self.r = r

