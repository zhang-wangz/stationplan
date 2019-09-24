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
    num = int(num)
    data, stationlist = getInfoStation()
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
    data, stationlist = getInfoStation()
    print(start not in stationlist.keys() and end not in stationlist.keys)
    if (not start or not end) or (start not in stationlist.keys() or end not in stationlist.keys()):
        result = {
            "code": 501,
            "msg": "please input the correct start and end station -.-"
        }
    else:
        stationnum, strmsg = getShort(start, end)
        result = {
            "code": 0,
            "msg": strmsg,
            "stationnum": stationnum
        }

    return json.dumps(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
