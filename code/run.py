import paho.mqtt.client as mqtt
import datetime
import time
import ssl
from enum import Enum

MQTT_TOPIC = '#'

def on_connect(mq, data, rc, _):
    global MQTT_TOPIC

    print('mqtt connected')
    mqtt_publish('mqtt_test', 'connected', 0, 0)

def on_message(mq, data, msg):
    print('topic: ', msg.topic)

def mqtt_publish(topic, msg, qos, retain):
    mqttClient.publish(topic, msg, qos, retain)

def mqttInit():
    mqttClient = mqtt.Client('device1')
    mqttClient.username_pw_set('device1', 'device1HKU')
    mqttClient.on_connect = on_connect
    mqttClient.on_message = on_message
    #
    mqttClient.tls_set(ca_certs='../mq.crt', tls_version=ssl.PROTOCOL_TLSv1_2)
    #
    mqttClient.tls_insecure_set(False)
    mqttClient.connect(host='sphku.com',port=8883)
    mqttClient.loop_start()
    return mqttClient

try:
    # connect mqtt broker
    mqttClient = mqttInit()

    # # forever loop
    # while True:
    #     time.sleep(2)

# ctrl-c
except KeyboardInterrupt:
    if (mqttClient.is_connected() == True):
        mqtt_publish('mqtt_test', 'program exit', 0, 0)
        mqttClient.disconnect()
        time.sleep(1)