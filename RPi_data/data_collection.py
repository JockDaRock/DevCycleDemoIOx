async_mode = None

if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()


import RPi.GPIO as GPIO
import json
import paho.mqtt.client as mqtt
import sys
import time
from threading import Thread
from flask import Flask, request


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
thread = None

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

hallsensor = 15

rpm = 0.0000
MPH = 0.0000
cad = 0.0000
dist = 0.0000
maxSpeed = 0.0000
racerTime = 0.0000
riderUserID = 'DevNet'
maxSpeedThresh = False
distThresh = False
newRider = False
ReservationID = ''

mqttc = mqtt.Client()
mqttc.connect("192.168.195.7")  #<--- Please change IP to match the location of your MQTT broker
mqttc.loop_start()

GPIO.setup(hallsensor, GPIO.IN, GPIO.PUD_UP)


def background_thread():
    global newRider
    global rpm
    global MPH
    global cad
    global dist
    global maxSpeed
    global racerTime
    global riderUserID
    global maxSpeedThresh
    global distThresh
    global messagechannel

    racerTime = time.time()
    t0 = time.time()
    GPIO.add_event_detect(hallsensor, GPIO.FALLING)

    while True:

        time.sleep(0)
        t1 = time.time()
        try:
            channel = GPIO.wait_for_edge(hallsensor,
                                         GPIO.FALLING,
                                         timeout=5000)
            if channel != None:
                rpm = round((1 / ((t1 - t0) / 60)), 2)
                cad = round(rpm * 0.29268292682927, 2)
                MPH = round(((rpm * 60 * 26 * 3.14159265) / (12 * 5280)), 2)
                dist += ((26 * 3.14159265) / (12 * 5280))
                if maxSpeed < MPH:
                    maxSpeed = MPH
                else:
                    pass
                socketData(rpm, MPH, cad, dist, maxSpeed)
                brokerMessage = {"RiderName": riderUserID,
                                 "rpm": rpm,
                                 "cadence": cad,
                                 "MPH": MPH,
                                 "dist": round(dist, 2),
                                 "maxSpeed": maxSpeed,
                                 "maxSpeedThresh": maxSpeedThresh,
                                 "distThresh": distThresh,
                                 "RawRevolution": 1.00,
                                 "RawCadence": 0.29268292682927,
                                 "RawDistance": (26 * 3.14159265) / (12 * 5280),
                                 "ReservationID": ReservationID
                                 }
                mqttc.publish("test/test", json.dumps(brokerMessage))
                t0 = t1
            else:
                brokerMessage = {"RiderName": riderUserID,
                                 "rpm": 0,
                                 "cadence": 0,
                                 "MPH": 0,
                                 "dist": dist,
                                 "maxSpeed": maxSpeed,
                                 "maxSpeedThresh": maxSpeedThresh,
                                 "distThresh": distThresh,
                                 "RawRevolution": 0,
                                 "RawCadence": 0,
                                 "RawDistance": 0,
                                 "ReservationID": ReservationID
                                 }
                mqttc.publish("test/test", json.dumps(brokerMessage))
        except KeyboardInterrupt:
            connection.close()
            GPIO.cleanup()
            sys.exit(0)


@app.route('/resetrider', methods=['GET', 'POST'])
def allThingsMadeNew():
    global newRider
    global racerTime
    global distThresh
    global maxSpeedThresh
    global riderUserID
    global cad
    global rpm
    global MPH
    global dist
    global maxSpeed
    global messagechannel
    global ReservationID

    try:
        riderRequest = request.json
    except BaseException as e:
        riderRequest = json.dumps({'Username': 'DevNet', 'ReservationID': 'GeneralDevNetUser'})

    runSpeed = False
    runDistance = False

    racerTime = 0.0000
    distThresh = False
    maxSpeedThresh = False
    rpm = 0.0000
    MPH = 0.0000
    cad = 0.0000
    dist = 0.0000
    maxSpeed = 0.0000
    riderUserID = riderRequest['Username']
    ReservationID = riderRequest['ReservationID']

    brokerMessage = {"RiderName": riderUserID,
                     "rpm": rpm,
                     "cadence": cad,
                     "MPH": MPH,
                     "dist": round(dist, 2),
                     "maxSpeed": maxSpeed,
                     "maxSpeedThresh": maxSpeedThresh,
                     "distThresh": distThresh,
                     "RawRevolution": 1.00,
                     "RawCadence": 0.29268292682927,
                     "RawDistance": (26 * 3.14159265) / (12 * 5280),
                     "runSpeed": runSpeed,
                     "runDistance": runDistance,
                     "ReservationID": ReservationID
                     }

    mqttc.publish("test/test", json.dumps(brokerMessage))

    return jsonify({'message': Success})


if __name__ == '__main__':
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()
    app.run(debug=False, host="0.0.0.0", port=5555)

