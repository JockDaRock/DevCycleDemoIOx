import twitter
import paho.mqtt.client as mqtt
import requests
import json


api = twitter.Api(consumer_key='YourKey',
                  consumer_secret='YourSecret',
                  access_token_key='appKey',
                  access_token_secret='AppSecret')

visitors = 1
with open(filename, 'r+') as f:
    f.write(visitors)

while True:
    with open(filename, 'r+') as f:
        text = f.read()
        f.seek(0)
        f.write(text)
        f.truncate()
    visitors += 1
    status = api.PostUpdate('')
    print(status.text)


runSpeed = False
runDistance = False
ReservationID = ''


def theMagic():
    magicHeaders = {"Accept": "application/json", "APIkey": "endpoint12345"}
    magicURL = "http://10.10.20.5:8181/AutomationFX/api/phones/SEP881DFC60ED16/calls/5557"
    print(magicURL)
    try:
        magicReq = requests.post(magicURL, headers=magicHeaders)

        magicResp = magicReq.content

        print(magicResp)

        return
    except BaseException as e:
        print(e)
        return


def moreMagic():
    magicHeaders = {"Accept": "application/json", "APIkey": "endpoint12345"}
    magicURL = "http://10.10.20.5:8181/AutomationFX/api/phones/SEP881DFC60ED16/calls/5558"
    print(magicURL)
    try:
        magicReq = requests.post(magicURL, headers=magicHeaders)

        magicResp = magicReq.content

        print(magicResp)

        return
    except BaseException as e:
        print(e)
        return


def on_connect(client, userdata, flags, rc):
    #print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("test/test")


def on_message(client, userdata, msg):
    global runDistance
    global runSpeed
    global ReservationID
    body = json.loads(str(msg.payload))

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

    if cad >= 75 and runSpeed == False:
        print(' [x] %r Wheel RPM, %r Cadence, %r MPH, %r distance, %r Max Speed' % (rpm, cad,
                                                                                    MPH, dist,
                                                                                    maxSpeed))
        theMagic()
        """Mess = "You initiated the Tropo API Call, Don't Bite the Dust!"
        try:
            csOutPutWindow(ReservationID, Mess)
        except Exception as e:
            pass"""
        runSpeed = True
    elif dist > 0.2 and runDistance == False:
        print(' [x] %r Wheel RPM, %r Cadence, %r MPH, %r distance, %r Max Speed' % (rpm, cad,
                                                                                    MPH, dist,
                                                                                    maxSpeed))
        moreMagic()
        """Mess = "You initiated the UnifiedFX API Call, Enjoy the Video!"
        try:
            csOutPutWindow(ReservationID, Mess)
        except Exception as e:
            pass"""
        runDistance = True

    else:
        print(' [x] %r Wheel RPM, %r Cadence, %r MPH, %r distance, %r Max Speed' % (rpm, cad,
                                                                                    MPH, dist,
                                                                                    maxSpeed))

client_mqtt = mqtt.Client()
client_mqtt.on_connect = on_connect
client_mqtt.on_message = on_message

client_mqtt.connect("192.168.195.7", 1883, 60)


def main():
    client_mqtt.loop_forever()


if __name__ == '__main__':
    main()
