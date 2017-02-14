import paho.mqtt.client as mqtt
import requests
import json
#import cloudshell.helpers.scripts.cloudshell_scripts_helpers as helper
import sys

runSpeed = True
runDistance = True
ReservationID = ''


"""def csOutPutWindow(ReservationID, Mess):
    # Load sensitive server info from file
    f = open('ServerInfo.txt', 'r')
    print(ReservationID)
    input = json.loads(f.read())
    serverAddress = input['Address']
    print(serverAddress)
    serverUser = input['User']
    print(serverUser)
    serverPassword = input['Password']
    print(serverPassword)
    domain = input['Domain']
    print(domain)

    # Reservation ID provided by script
    resId = ReservationID
    challenge = 'Tropo Call Initiated!'

    # HTML Formatting - top of HTML doc
    topHTML = """<html>
    <head>
    <script></script>
    </head>
    <body>
       <h2 style="color:green;" align="center">
    """
    # bike/challenge info to display
    midHTML = Mess

    # HTML Formatting - bottom of HTML doc
    botHTML = """</h2>
    <p></p>
    <p></p>
    <p></p>
    </body>
    </html>
    """

    # Inialize CS API Session
    api_session = helper.CloudShellAPISession(serverAddress, serverUser, serverPassword, domain)
    message = topHTML + midHTML + botHTML
    print(message)

    # Execute post to lab output window
    api_session.WriteMessageToReservationOutput(resId, message)"""


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
