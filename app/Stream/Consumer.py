"""
@author Aaditya and Sam Blesswin
@version 0.1
@since 17-03-2024
NOT FOR USE, THIS IS ONLY TEST CODE
"""

from confluent_kafka import Consumer, KafkaError
import sys

# Consumer setup.
config = {
    "bootstrap.servers": "0.0.0.0:9092",
    "group.id": "my_consumer_group",
    "auto.offset.reset": "earliest",
}

# Define the topic to which you want to consume messages
topic = "ecommerce_activity"

consumer = Consumer(config)
consumer.subscribe([topic])

# Read
try:
    while True:
        msg = consumer.poll(timeout=1.0)  # Poll for messages with a timeout of 1 second

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition, consumer has reached the end
                continue

        print(f"Received message: {msg.value().decode('utf-8')}")

except KeyboardInterrupt:
    pass

finally:
    consumer.close()
