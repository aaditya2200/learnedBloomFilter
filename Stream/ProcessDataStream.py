from kafka import KafkaConsumer, KafkaProducer
import random
import string
import sys
from json import dumps

def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


# Bootstrap server configuration.
bootstrap_servers = ['localhost:9092']

# Topic Name
topic_name = 'quickstart-events'

# producer setup
kafka_producer = KafkaProducer(bootstrap_servers=bootstrap_servers, value_serializer=lambda x: dumps(x).encode('utf-8'))
# send data to the topic
try:
    while True:
        ack = kafka_producer.send(topic_name, generate_random_string(10).encode('utf-8'))
        metadata = ack.get()
        print(metadata.topic, metadata.partition)
except KeyboardInterrupt:
    sys.exit()

