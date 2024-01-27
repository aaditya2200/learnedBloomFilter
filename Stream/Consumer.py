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
