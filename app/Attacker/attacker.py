"""
@author Aaditya and Sam Blesswin
"""

# This script is the attacker script.
# It will probe the filter until it identifies an False Positive (FP) key.
# Once it does, it will keep querying with the same key.

import requests
import numpy as np

# from Hashes import hash

base_url = "http://flaskapp:5001"


class Attacker:
    def __init__(self):
        self.false_positives_average_poll_list_lbf = []
        self.false_positives_average_poll_list_bf = []
        return

    def attack(self, limit):
        self.false_positives_average_poll_list_lbf = [0] * int(limit)
        counter = 1
        index = 0
        attempts = 0
        while True:
            attempts += 1
            if attempts > int(limit):
                break
            response = requests.get(f"{base_url}/query/{counter}")
            if response.json()["Present"] and not response.json()["found_in_db"]:
                while True:
                    attempts += 1
                    if attempts > int(limit):
                        break
                    response = requests.get(f"{base_url}/query/{counter}")
                    if not response.json()["Present"]:
                        index += 1
                        break
                    self.false_positives_average_poll_list_lbf[index] += 1
                # We have found a FP key. Keep querying with this key
            else:
                counter += 1
        print('')

    def attack_normal(self, limit):
        self.false_positives_average_poll_list_bf = [0] * int(limit)
        counter = 1
        index = 0
        attempts = 0
        while True:
            attempts += 1
            if attempts > int(limit):
                break
            response = requests.get(f"{base_url}/query-normal/{counter}")
            if response.json()["Present"] and not response.json()["found_in_db"]:
                while True:
                    attempts += 1
                    if attempts > int(limit):
                        break
                    response = requests.get(f"{base_url}/query-normal/{counter}")
                    if not response.json()["Present"]:
                        index += 1
                        break
                    self.false_positives_average_poll_list_bf[index] += 1
                # We have found a FP key. Keep querying with this key
            else:
                counter += 1
        print('')

    def report(self):
        mean1 = max(self.false_positives_average_poll_list_lbf)
        mean2 = max(self.false_positives_average_poll_list_bf)
        memory = requests.get(f"{base_url}/mem")
        # Plot the means on a bar graph
        print('Mean attempts on the same key for learned broom filter {}'.format(mean1))
        print('Mean attempts on the same key for bloom filter {}'.format(mean2))
        print('Memory usage {}'.format(memory.json()['memory']))
        return {
            'learned_filter': mean1,
            'bloom_filter': mean2,
            'memory_usage': memory.json()['memory']
        }
