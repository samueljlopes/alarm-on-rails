# Code snippet for Kafka client in Python - replicated in Javascript

from confluent_kafka import Consumer
from pathlib import Path
import argparse
import warnings
warnings.filterwarnings('ignore')

from lxml import etree 
import json

import pprint

BOOTSTRAP_SERVER = 'pkc-l6wr6.europe-west2.gcp.confluent.cloud:9092'
GROUP_ID = 'SC-d57fba73-347c-4a1b-b51b-7d94fee61fac'
SASL_USERNAME = '4B6AUSNDI572IKKY'
SASL_PASSWORD = 'Gkdxy4W+RC/2cotb3KGViodZBE91S+/WqFqB8U0Gm7xLqQpwDWnn7ePrm18mqsxp'
SSL_CA_LOCATION = '/Users/samuellopes/Documents/GitHub/alarm-on-rails/backend/cacert-2024-11-26.pem'
TOPIC_NAME = 'prod-1010-Darwin-Train-Information-Push-Port-IIII2_0-XML'

config = {
    'bootstrap.servers': BOOTSTRAP_SERVER,
    'group.id': GROUP_ID,
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': SASL_USERNAME,
    'sasl.password': SASL_PASSWORD,
    'ssl.ca.location': SSL_CA_LOCATION,
    #'auto.offset.reset': 'earliest'
}

consumer = Consumer(config)
consumer.subscribe([TOPIC_NAME])

l = []
count = 0
try:
    while True:
        msg = consumer.poll(1.0)
        if msg is not None and msg.error() is None:
            key = msg.key()
            value = msg.value()
            try:
                if key is not None:
                    key = key.decode('utf-8')
            except:
                key = "None"
            try:
                if value is not None:
                    value = value.decode('utf-8')
            except:
                value = "None"
            # print("key = {key:12} value = {value:12}".format(key, value))

            valueJSON = json.loads(str(value))
            messageTree = etree.fromstring(bytes(valueJSON['bytes'], 'utf-8'))
            prettyMessageTree = etree.tostring(messageTree, pretty_print = True, encoding = str)

            print(prettyMessageTree)

            l.append(messageTree)
            count+=1

finally:
    consumer.close()

