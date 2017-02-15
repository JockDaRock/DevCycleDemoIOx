from pymongo import MongoClient
import paho.mqtt.client as mqtt
import json


client_db = MongoClient('mongodb://192.168.194.9:27017/database')

db = client_db.test


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("test/test")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global db
    body = json.loads(msg.payload.decode('unicode_escape'))
    result = db.berlin.insert_one(body)

client_mqtt = mqtt.Client()
client_mqtt.on_connect = on_connect
client_mqtt.on_message = on_message

client_mqtt.connect("192.168.195.7", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client_mqtt.loop_forever()