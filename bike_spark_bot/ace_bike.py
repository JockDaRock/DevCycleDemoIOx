import paho.mqtt.client as mqtt
import requests
import json

runSpeed = False
runDistance = False
ReservationID = ''

token = "Bearer <token>"
room = "<room id>"


def spark_it(message, bot_token, roomid):
    start_url = "https://api.ciscospark.com"

    token = bot_token

    header = {"Authorization": "%s" % token,
              "Content-Type": "application/json"}

    api_url = "/v1/messages/"
    data = {"roomId": roomid,
            "text": message}

    spark_url = start_url + api_url

    spark_message = requests.post(spark_url, headers=header, data=json.dumps(data), verify=True)

    return spark_message


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

        kph = str(MPH * 1.6)
        spark_it("You just went %s KPH" % kph, token, room)
        runSpeed = True
    elif dist > 0.2 and runDistance == False:
        print(' [x] %r Wheel RPM, %r Cadence, %r MPH, %r distance, %r Max Speed' % (rpm, cad,
                                                                                    MPH, dist,
                                                                                    maxSpeed))
        spark_it("You just went %s KPH" % kph, token, room)
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
