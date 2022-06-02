import paho.mqtt.client as mqtt
import datetime
import time
import ssl
from enum import Enum
import random

source = 'https://www.emqx.com/en/blog/how-to-use-mqtt-in-python'

MQTT_HOST = 'sphku.com'
MQTT_PORT = 8883
MQTT_TOPIC = '#'
MQTT_CLIENT_ID = f'python-mqtt-{random.randint(0, 1000)}'
MQTT_USERNAME = 'device1'
MQTT_PASSWORD = 'device1HKU'

MQTT_CERT = '../mq.crt'

def on_connect(mq, data, rc, _):
    global MQTT_TOPIC

    print('mqtt connected')
    mqtt_publish('mqtt_test', 'connected', 0, 0)

def on_message(mq, data, msg):
    print('topic: ', msg.topic)

def mqtt_publish(topic, msg, qos, retain):
    mqttClient.publish(topic, msg, qos, retain)

def mqttInit():
    mqttClient = mqtt.Client(MQTT_CLIENT_ID)
    mqttClient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    mqttClient.on_connect = on_connect
    mqttClient.on_message = on_message
    mqttClient.tls_set(ca_certs = MQTT_CERT, tls_version = ssl.PROTOCOL_TLSv1_2)
    mqttClient.tls_insecure_set(False)
    mqttClient.connect(host = MQTT_HOST, port = MQTT_PORT)
    mqttClient.loop_start()
    return mqttClient

try:
    # connect mqtt broker
    mqttClient = mqttInit()

    # forever loop
    while True:
        time.sleep(2)

# ctrl-c
except KeyboardInterrupt:
    if (mqttClient.is_connected() == True):
        mqtt_publish('mqtt_test', 'program exit', 0, 0)
        mqttClient.disconnect()
        time.sleep(1)