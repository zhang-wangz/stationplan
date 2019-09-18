# encoding=utf-8
import os
import json

from stationplan import computefshortestpath
from stationplan import getInfo


def getShort(start, end):
    a, s = computefshortestpath(start, end)
    return s


def getInfoStation():
    stationlist = getInfo()
    return stationlist


if __name__ == "__main__":
    a = input()
    b = input()
    s = getShort(a, b)
    print(s)
    # print(getInfoStation())
