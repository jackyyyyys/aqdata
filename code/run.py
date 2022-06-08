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

### retracing warning
source = 'https://www.emqx.com/en/blog/how-to-use-mqtt-in-python'

sensors = ['4C11AEE82D80', '98F4AB38C884', '98F4AB39DB50']
MQTT_HOST = 'sphku.com'
MQTT_PORT = 8883
MQTT_TOPIC_SUBSCRIBE = [
                        (f'hku/sensor/{sensors[0]}/data', 0),
                        (f'hku/sensor/{sensors[1]}/data', 0),
                        (f'hku/sensor/{sensors[2]}/data', 0)
                    ]
MQTT_TOPIC_PUBLISH = 'hku/sensor/{sensor}/ranking'
MQTT_CLIENT_ID = f'python-mqtt-{random.randint(0, 1000)}'
MQTT_USERNAME = 'device1'
MQTT_PASSWORD = 'device1HKU'
MQTT_CERT = '../mq.crt'

def mqtt_publish(client, topic, message):
    result = client.publish(topic, message)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{message}` to `{topic}`")
    else:
        print(f"Failed to send message to {topic}")

def mqtt_subscribe(client: mqtt_client):
    def on_subscribe(client, userdata, mid, granted_qos):
        print('Subscription running ', mid, granted_qos)

    def on_message(client, userdata, msg):
        print(f"Received `{json.loads(msg.payload)}` from `{msg.topic}`")
        sensor = msg.topic[11:23]
        rank_req = json.loads(msg.payload)
        rank = quality(sensors.index(sensor)+1, rank_req['CO2'], rank_req['VOC'], rank_req['RH'], rank_req['TEM'], rank_req['PM25'])
        print(f'Prediction of sensor {sensor} > Rank: {rank}')
        rank_res = {
            'sensor': sensor,
            'ts': rank_req['TIME'],
            'rank': int(round(rank))
        }
        mqtt_publish(client, MQTT_TOPIC_PUBLISH.replace('{sensor}', sensor), json.dumps(rank_res))

    # subscribe to 
    client.subscribe(MQTT_TOPIC_SUBSCRIBE)

    client.on_message = on_message
    client.on_subscribe = on_subscribe

def mqtt_connect() -> mqtt_client:
    def on_connect(mq, data, rc, _):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")
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
    mqtt_subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()
