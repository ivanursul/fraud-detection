import json
from kafka import KafkaProducer
import numpy as np

# def np_encoder(object):
#     if isinstance(object, np.generic):
#         return object.item()


def json_serializer(data):
    return json.dumps(data, default=str).encode('utf-8')


producer = KafkaProducer(
    bootstrap_servers=['localhost:9093'],  # Update the port if your Kafka runs on a different one
    value_serializer=json_serializer
)


def publish_message(topic_name, value):
    producer.send(topic_name, value)
    producer.flush()