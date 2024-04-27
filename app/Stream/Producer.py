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
topic = "ecommerce_activity"


def get_random_element(lst):
    return random.choice(lst)


def generate_activity():
    return {
        "userId": random.randint(0, 999999),
        "activityType": get_random_element(activity_types),
        "productId": f"product{random.randint(0, 999)}",
        "timestamp": datetime.utcnow().isoformat(),
        "category": get_random_element(categories),
        "price": random.uniform(0, 1200),
        "location": get_random_element(locations),
        "device": get_random_element(devices),
    }


def produce_message():
    try:
        message = generate_activity()
        producer.produce(topic, key=message["userId"], value=json.dumps(message))
        producer.flush()
    except Exception as e:
        print(f"Failed to send message: {e}")


def produce_end_message():
    try:
        producer.produce(topic, key=-1, value=json.dumps({"message": "end"}))
        producer.flush()
    except Exception as e:
        print(f"Failed to send message: {e}")


def run():
    counter = 0
    while counter < 100:  # while true
        produce_message()
        counter += 1
    produce_end_message()
