# encoding=utf-8
from flask import Flask, request
from stationController import getShort
from stationController import getInfoStation
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello Flask!'


@app.route('/getStationInfo', methods=['GET'])
def getStationInfo():
    num = request.args["num"]
    data = getInfoStation()
    num = int(num)
    if not num:
        result = {
            "code": 500,
            "msg": "the service make a mistake -.-"
        }
    else:
        strmsg = data[num]
        print(strmsg)
        result = {
            "code": 0,
            "msg": strmsg
        }
    return json.dumps(result)


@app.route('/getShortestPath', methods=['GET'])
def getShortestPath():
    start = request.args['start']
    end = request.args['end']
    # request.form['start']
    if not start or not end:
        result = {
            "code": 500,
            "msg": "the service make a mistake -.-"
        }
    else:
        strmsg = getShort(start, end)
        result = {
            "code": 0,
            "msg": strmsg
        }

    return json.dumps(result)


if __name__ == '__main__':
    app.run()
