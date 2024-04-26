"""
@author Aaditya and Sam Blesswin
@version 0.1
@since 17-03-2024
"""

from confluent_kafka import Producer
import json



if __name__ == '__main__':
    # Create Producer instance
    producer = Producer({'bootstrap.servers': 'localhost:9092'})

    # Define the topic to which you want to produce messages
    topic = 'stream-test'

    # Define your JSON data
    data = {
        "key": 12345,
        "value": "example_value"
    }

    # Serialize the data to JSON
    json_data = json.dumps(data)

    # Produce the message with a key
    producer.produce(topic, key=str(data["key"]), value=json_data)

    # Flush messages to ensure they are sent
    producer.flush()