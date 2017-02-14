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


import json
import sys
from threading import Thread
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from pymongo import MongoClient
import pymongo
import socketio


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
global thread
thread = None


def background_thread():

    while True:
        client = MongoClient()

        db = client.test

        data = []
        jsondata = []

        """cursor = db.berlin.find().sort([
            ("Rider", pymongo.DESCENDING),
            ("maxSpeed", pymongo.DESCENDING),
            ("dist", pymongo.DESCENDING)
        ]).distinct('RiderName')"""

        cursor = db.berlin.distinct('RiderName')

        for i in range(0, len(cursor)):
            cursor1 = db.berlin.find({'RiderName': cursor[i]}).sort([
                ("dist", pymongo.DESCENDING)
            ])
            # data.append({cursor1[0]['dist']: {'Dist': cursor1[0]['dist'], 'RiderName': cursor1[0]['RiderName']}})
            data.append({'Dist': cursor1[0]['dist'], 'RiderName': cursor1[0]['RiderName']})

        data.sort(reverse=True)

        if len(data) > 6:
            for j in range(0, 6):
                jsondata.append(data[j])

        else:
            for j in range(0, len(data)):
                jsondata.append(data[j])

        jsondata = json.dumps(jsondata)

        try:
            socketData(jsondata)
        except KeyboardInterrupt:
            connection.close()
            GPIO.cleanup()
            sys.exit(0)


def socketData(jsondata):
    socketio.emit('my response',
                  {'data': 'Server generated event',
                   'jsondata': jsondata},
                  namespace='/dbdata',
                  broadcast=True,
                  )


@app.route('/')
def index():
    return "DevNet Rocks"


@socketio.on('connect')
def dbsocket():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()


if __name__ == '__main__':
    socketio.run(app, debug=False, host="0.0.0.0", port=5050)





