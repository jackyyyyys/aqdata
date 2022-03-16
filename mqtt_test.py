import datetime
import logging
import os
import time
import json
from enum import Enum
import ssl

import paho.mqtt.client as mqtt

# Constants
LOG_FORMAT = '%(asctime)-15s : %(levelname)s : %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_FILENAME = datetime.datetime.now().strftime('log/%Y%m%d_%H%M%S.log')
LOG_ID = 'mqtt2db'

MQTT_TOPIC = '#'

'''
MQTT Functions
'''
def on_connect(mq, data, rc, _):
    global MQTT_TOPIC

    print('mqtt connected')
    # subscribe when connected
    mq.subscribe(MQTT_TOPIC)
    mqtt_pub('mqtt_test', 'connected', 0, 0)

def on_message(mq, data, msg):
    print('topic: ', msg.topic)

def on_log(mq, data, level, buf):
    print('log: ', buf)
    pass

def mqtt_pub(topic, msg, qos, retain):
    mqttClient.publish(topic, msg, qos, retain)

def mqttInit():
    mqttClient = mqtt.Client('device1')
    mqttClient.username_pw_set('device1', 'device1HKU')
    mqttClient.on_connect = on_connect
    mqttClient.on_message = on_message
    mqttClient.on_log = on_log
    #
    mqttClient.tls_set(ca_certs='mq.crt', tls_version=ssl.PROTOCOL_TLSv1_2)
    #
    mqttClient.tls_insecure_set(False)
    mqttClient.connect(host='sphku.com',port=8883)
    mqttClient.loop_start()
    return mqttClient

# Init Logger
# Create log folder if not exist
os.makedirs(os.path.dirname(LOG_FILENAME), exist_ok=True)
# file logger
logging.basicConfig(format=LOG_FORMAT,
                level=LOG_LEVEL,
                filename=LOG_FILENAME)
# console logger
console = logging.StreamHandler()
console.setLevel(LOG_LEVEL)
console.setFormatter(logging.Formatter(LOG_FORMAT))
logger = logging.getLogger(LOG_ID)
logger.addHandler(console)

logger.info('mqtt_test starting...')

try:
    # connect mqtt broker
    logger.info('mqtt connecting...')
    mqttClient = mqttInit()

    # forever loop
    while True:
        time.sleep(2)

# ctrl-c
except KeyboardInterrupt:
    logger.debug('User abort.')
    if (mqttClient.is_connected() == True):
        mqtt_pub('mqtt_test', 'program exit', 0, 0)
        mqttClient.disconnect()
        time.sleep(1)
    logger.info('Exit program')
