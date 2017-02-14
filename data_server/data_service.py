import paho.mqtt.client as mqtt
import json
import eventlet
from threading import Thread

from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

async_mode = 'eventlet'
eventlet.monkey_patch()
thread = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
client = mqtt.Client()


def socketData(rpm, MPH, cad, dist, maxSpeed):
    emit('my response',
         {'data': 'Server generated event',
          'rpm': rpm,
          'MPH': MPH,
          'cadence': cad,
          'dist': dist,
          'maxSpeed': maxSpeed},
         namespace='/test',
         broadcast=True,
         )


def on_connect(client, userdata, flags, rc):
    print("Connected with result " + str(rc))

    client.subscribe("test/test")


def on_message(client, userdata, msg):
    body = json.loads(msg.payload)
    try:
        runSpeed = body["runSpeed"]
        runDistance = body["runDistance"]
        ReservationID = body["ReservationID"]
        rpm = body["rpm"]
        cad = body["cadence"]
        MPH = body["MPH"]
        dist = body["dist"]
        maxSpeed = body["maxSpeed"]

    except Exception as e:
        rpm = body["rpm"]
        cad = body["cadence"]
        MPH = body["MPH"]
        dist = body["dist"]
        maxSpeed = body["maxSpeed"]

    socketData(rpm, MPH, cad, dist, maxSpeed)


def mqtt_consumer():
    with app.test_request_context():  #<-- This is needed to include the mqtt thread in the same context as the flask app, allowing it to call functions and data from our fask instance.
        client.loop_forever()


def background_thread():
    global client
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("192.168.195.7", 1883, 60)

    while True:
        try:
            mqtt_consumer()
        except KeyboardInterrupt:
            print("Disconnected")


@socketio.on('connect')
def socket_start():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()


if __name__ == '__main__':
    socketio.run(app, debug=False, host="0.0.0.0", port=8000)
