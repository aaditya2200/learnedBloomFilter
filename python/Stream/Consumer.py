"""
@author Aaditya
@version 0.1
@since 17-03-2024
NOT FOR USE, THIS IS ONLY TEST CODE
"""
from kafka import KafkaConsumer, KafkaProducer
import sys
# Consumer setup.
bootstrap_servers = ['localhost:9092']

topic_name = 'quickstart-events'

consumer = KafkaConsumer(topic_name, bootstrap_servers= bootstrap_servers)

# Read
try:
    for message in consumer:
        print(message.value)
except KeyboardInterrupt:
    sys.exit()
