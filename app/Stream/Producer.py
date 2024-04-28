"""
@author Aaditya and Sam Blesswin
@version 0.1
@since 17-03-2024
"""

from confluent_kafka import Producer
import json
from datetime import datetime
import random
import time

key_distributions = ['random', 'gaussian', 'binomial', 'poisson']

activity_types = ["view", "click", "purchase"]
categories = [
    "electronics",
    "fashion",
    "furniture",
    "toys",
    "books",
    "home appliances",
    "sports",
    "automotive",
    "jewelry",
    "travel",
    "party supplies",
]
devices = ["android", "ios", "mac", "windows", "linux"]
locations = [
    "New York",
    "Los Angeles",
    "SaltLakeCity",
    "Chicago",
    "Boston",
    "Newyork",
    "Houston",
    "Phoenix",
    "Philadelphia",
    "San Antonio",
    "San Diego",
    "Dallas",
    "San Jose",
    "Austin",
    "San Francisco",
    "Indianapolis",
    "Colorado",
]

config = {"bootstrap.servers": "kafka:9092", "client.id": "my-ecommerce-app"}

# Create Producer instance
producer = Producer(config)

# Define the topic to which you want to produce messages
topic = "ecommerce-activity"

def generate_prime():
    yield 2  # 2 is the first prime number
    sieve = {}  # Using a dictionary to store multiples of primes
    num = 3  # Start checking from 3
    while True:
        if num not in sieve:
            yield num  # Yield the prime number
            sieve[num * num] = [num]  # Mark the square of the prime as a multiple
        else:
            for p in sieve[num]:  # Mark all multiples of the prime
                sieve.setdefault(num + p, []).append(p)
            del sieve[num]  # Remove the prime from the sieve
        num += 2  # Check only odd numbers (even numbers greater than 2 are not prime)

def generate_mix():
    yield 2
    yield 3
    sieve = {}
    num = 5
    while True:
        if num % 2 == 0:
            yield num
        elif num not in sieve:
            yield num
            sieve[num * num] = [num]
        else:
            for p in sieve[num]:
                sieve.setdefault(num + p, []).append(p)
            del sieve[num]
        num += 2  # Check only odd numbers (even numbers greater than 2 are not prime)

def generate_odd(limit):
    for i in range (1, limit):
        if i % 2 != 0:
            yield i


def get_random_element(lst):
    return random.choice(lst)


def generate_activity(distribution, prime_gen, mix_gen, limit):
    if distribution == 'mix':
        user_id = next(mix_gen)
    elif distribution == 'prime':
        user_id = next(prime_gen)
    else:
        user_id = next(generate_odd(int(limit)))
    return {
        "userId": user_id,
        "activityType": get_random_element(activity_types),
        "productId": f"product{random.randint(0, 999)}",
        "timestamp": datetime.utcnow().isoformat(),
        "category": get_random_element(categories),
        "price": random.uniform(0, 1200),
        "location": get_random_element(locations),
        "device": get_random_element(devices),
    }


def produce_message(distribution, prime_gen, mix_gen, limit):
    try:
        message = generate_activity(distribution, prime_gen, mix_gen, limit)
        producer.produce(topic, key=str(message["userId"]).encode('utf-8'), value=json.dumps(message))
        producer.flush()
    except Exception as e:
        print(f"Failed to send message: {e}")


def produce_end_message():
    try:
        producer.produce(topic, key=str(-1).encode('utf-8'), value=json.dumps({"message": "end"}))
        producer.flush()
    except Exception as e:
        print(f"Failed to send message: {e}")


def run(distribution, limit):
    counter = 0
    prime_gen = generate_prime()
    mix_gen = generate_mix()
    while counter < int(limit):  # while true
        produce_message(distribution, prime_gen, mix_gen, limit)
        counter += 1
    produce_end_message()
