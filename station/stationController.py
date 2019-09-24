# encoding=utf-8
import os
import json

from stationplan import computefshortestpath
from stationplan import getInfo


def getShort(start, end):
    stationnum, s = computefshortestpath(start, end)
    return stationnum, s


def getInfoStation():
    stationnumlist, stationlist = getInfo()
    return stationnumlist, stationlist


if __name__ == "__main__":
    # a = input()
    # b = input()
    # s = getShort(a, b)
    # print(s)
    a, b = getInfoStation()
    print(type(a))
    print(type(b))
