"""
@author Aaditya and Sam Blesswin
"""

# This script is the attacker script.
# It will probe the filter until it identifies an False Positive (FP) key.
# Once it does, it will keep querying with the same key.

from interface import api
import json

# from Hashes import hash


class Attacker:
    def __init__(self):
        return

    def attack(self):
        # hash_lib = hash.Hash()
        # even_numbers = []
        # odd_numbers = []
        # # Generate even and odd numbers between 0 and 9999
        # for num in range(1000):
        #     if num % 2 == 0:
        #         even_numbers.append(num)
        #     else:
        #         odd_numbers.append(num)

        # # Create the filter
        # lbf = api.LearnedBloomFilter(api.MODE.DEBUG)
        # for item in odd_numbers:
        #     lbf.insert(item)

        # For simplicity, we are providing the filter the domain of the keys. Without this information,
        # it is very time-consuming for the attacker to identify which key is a false positive.

        counter = 0
        while True:
            response = lbf.query(counter)
            if response.json["Present"] and not response.json["found_in_db"]:
                while True:
                    response = lbf.query(counter)
                    if not response.json["Present"]:
                        break
                # We have found a FP key. Keep querying with this key
            else:
                counter += 1
