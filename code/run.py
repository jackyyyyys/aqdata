import paho.mqtt.client as mqtt_client
import datetime
import time
import ssl
from enum import Enum
import random

source = 'https://www.emqx.com/en/blog/how-to-use-mqtt-in-python'

MQTT_HOST = 'sphku.com'
MQTT_PORT = 8883
MQTT_TOPIC_PUBLISH = 'test/test'
MQTT_TOPIC_SUBSCRIBE = 'hk_retain/hku/DF9A5B9BF5E8F190D6E9F39B1A449F39/go_dest'
MQTT_CLIENT_ID = f'python-mqtt-{random.randint(0, 1000)}'
MQTT_USERNAME = 'device1'
MQTT_PASSWORD = 'device1HKU'

MQTT_CERT = '../mq.crt'

def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(MQTT_TOPIC_PUBLISH, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{MQTT_TOPIC_PUBLISH}`")
        else:
            print(f"Failed to send message to topic {MQTT_TOPIC_PUBLISH}")
        msg_count += 1


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        # !!! here put use ML model code
        client.publish(client, "TEST")

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
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    run()
