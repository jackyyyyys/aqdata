import json
from flask import session
from matplotlib.font_manager import json_dump
import numpy
import paho.mqtt.client as mqtt_client
import datetime
import time
import ssl
from enum import Enum
import random
import pandas as pd
from test_use_model import quality

# how to get to know which sensor
# sub hku/sensor + switch or sub 3 topics?
TEMP_SESOR = "98F4AB38C884"
source = 'https://www.emqx.com/en/blog/how-to-use-mqtt-in-python'
sensor = TEMP_SESOR

SENSORS = { '4C11AEE82D80': 1, '98F4AB38C884': 2, '98F4AB39DB50': 3 }
MQTT_HOST = 'sphku.com'
MQTT_PORT = 8883
MQTT_TOPIC_SUBSCRIBE = f'hku/sensor/{sensor}/data'
MQTT_TOPIC_PUBLISH = f'hku/sensor/{sensor}/ranking'
MQTT_CLIENT_ID = f'python-mqtt-{random.randint(0, 1000)}'
MQTT_USERNAME = 'device1'
MQTT_PASSWORD = 'device1HKU'
MQTT_CERT = '../mq.crt'

def publish(client, message):
    result = client.publish(MQTT_TOPIC_PUBLISH, message)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{message}` to `{MQTT_TOPIC_PUBLISH}`")
    else:
        print(f"Failed to send message to {MQTT_TOPIC_PUBLISH}")

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}`")
        rank_req = json.loads(msg.payload)
        print(rank_req)
        # using traied ML model
        rank = quality(2, rank_req['CO2'], rank_req['VOC'], rank_req['RH'], rank_req['TEM'], rank_req['PM25'])
        print(rank)
        rank_res = {
            'sensor': sensor,
            'ts': rank_req['TIME'],
            'rank': int(round(rank))
        }
        publish(client, json.dumps(rank_res))

    # subscribe to 
    client.subscribe(MQTT_TOPIC_SUBSCRIBE)

    client.on_message = on_message

def mqtt_connect() -> mqtt_client:
    def on_connect(mq, data, rc, _):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
        print('mqtt connected')

    mqttClient = mqtt_client.Client(MQTT_CLIENT_ID)
    mqttClient.on_connect = on_connect
    mqttClient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    mqttClient.tls_set(ca_certs = MQTT_CERT, tls_version = ssl.PROTOCOL_TLSv1_2)
    mqttClient.tls_insecure_set(False)
    mqttClient.connect(host = MQTT_HOST, port = MQTT_PORT)
    return mqttClient

def run():
    client = mqtt_connect()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()
