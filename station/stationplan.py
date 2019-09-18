# encoding=utf-8
import os
import sys
import io
import numpy as np
import json
from Graph import Graph
from GraphAL import GraphAL
from GraphError import GraphError
from PrioQueue import PrioQueue

LINEDATA = ['1', '2', '3', '5', '6', '9']
STATION_NUM = {}
data = {}
datanum = {}

with open(os.path.join(os.path.abspath('..'), "station/stationLine.txt"), "r") as f:
    TOTAL = f.readline()
    for line in f.readlines():
        if line != '\n':
            line = line.rstrip('\n')
            line = line.split(' ')
            if line[0] in LINEDATA:
                linei = line[0]
                continue
            line[1] = linei
            line0 = line[0]

            intline = int(line[1])
            if intline not in data.keys():
                data[intline] = []
                data[intline].append(line0)
            else:
                data[intline].append(line0)
            if line0 not in datanum.keys():
                datanum[line0] = [intline]
            else:
                datanum[line0].append(intline)

i = 0
STATIO = {}
for datai in datanum.keys():
    STATION_NUM[datai] = i
    STATIO[i] = datai
    i += 1
I = i


# print("一共有" + str(I) + "站")


# 判断是否为环路,就是整条路线是一个
def iscircle(mlist):
    if mlist[0] == mlist[-1]:
        return True
    return False

#判断是否为换乘点
def istransport(station):
    if len(datanum[station])>1:
        return True
    return False

#得到换线路
def destransport(station):
    return datanum[station]


def changeline(p1,p2):
    line1=datanum[p1]
    line2=datanum[p2]
    a=[]
    for i1 in data[line1[0]]:
        if istransport(i1):
            ways=destransport(i1)
            for i2 in line2:
                if i2 in ways:
                    a.append(i1)
                    return i1
    return None

def getInfo():
    return data
# print("data", json.dumps(data, ensure_ascii=False))
# print("datanum", json.dumps(datanum, ensure_ascii=False))
# print("STATION_NUM", json.dumps(STATION_NUM, ensure_ascii=False))
# print("STATIO", json.dumps(STATIO, ensure_ascii=False))

# 设置所有相邻路线之间的边长
mat = np.full([i, i], np.inf)
# 以站点数量进行矩阵分布，141*141
RouteGraph = Graph(mat)
routee = {}
for key in data.keys():
    # datai 是每一条线路上的站点list
    datai = data[key]
    for i in range(1, len(datai) - 1):
        # RouteGraph.add_vertex()
        v1 = STATION_NUM[datai[i]]  # v1当前站点
        v2 = STATION_NUM[datai[i + 1]]  # v2后一个站点
        v3 = STATION_NUM[datai[i - 1]]  # v3前一个站点
        RouteGraph.add_edge(v1, v2, 1)
        RouteGraph.add_edge(v2, v1, 1)
        RouteGraph.add_edge(v3, v1, 1)
        RouteGraph.add_edge(v1, v3, 1)
    if iscircle(datai):
        # RouteGraph.add_vertex()
        v1 = STATION_NUM[datai[0]]
        v2 = STATION_NUM[datai[-2]]
        RouteGraph.add_edge(v1, v2, 1)
        RouteGraph.add_edge(v2, v1, 1)

def all_shortest_path(graph):
    import numpy as np
    vnum = graph.vertex_num()
    a = [[graph.get_edge(i, j) for j in range(vnum)] for i in range(vnum)]
    nvertex = [[-1 if a[i][j] == np.inf else j for j in range(vnum)] for i in range(vnum)]
    for k in range(vnum):
        for i in range(vnum):
            for j in range(vnum):
                if a[i][j] > a[i][k] + a[k][j]:
                    a[i][j] = a[i][k] + a[k][j]
                    nvertex[i][j] = nvertex[i][k]
    return a, nvertex

def find_shortest_path(graph, start, end, path=[]):
    # 查找最短路径
    path = path + [start]
    if start == end:
        return path
    if not start in graph.keys():
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest

def find_all_paths(graph, start, end, path):
    # 查找所有的路径
    path = path + [start]
    if start == end:
        return [path]
    if not start in graph.keys():
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths


# Dijkstra算法实现最短路径查找
pathss = {}
for i in range(I):
    for j in range(I):
        if RouteGraph.get_edge(i, j) == 1:
            start = STATIO[i]
            end = STATIO[j]
            if i not in pathss.keys():
                pathss[i] = [j]
            else:
                pathss[i].append(j)
# pathss是记录每个站点接触的站点list
# print(pathss)


def dijkstra_shortest_pathS(graph, v0, endpos):
    vnum = 0
    for i in pathss.keys():
        vnum += 1
    # print(vnum)
    # vnum=graph.vertex_num()
    assert 0 <= v0 < vnum
    # 长为vnum的表记录路径
    paths = [None] * vnum
    count = 0
    # 求解最短路径的候选边集记录在优先队列cands中（p,v,v'）v0经过v到v'的最短路径长度为p，根据p的大小排序，保证选到最近的未知距离顶点
    cands = PrioQueue([(0, v0, v0)])
    while count < vnum and not cands.is_empty():
        plen, u, vmin = cands.dequeue()  # 取路径最短顶点
        if paths[vmin]:  # 如果这个点的最短路径已知，则跳过
            continue
        paths[vmin] = (u, plen)  # 新确定最短路径并记录
        # print(u, plen)
        for v in graph[vmin]:  # 遍历经过新顶点组的路径
            if not paths[v]:  # 如果还不知道最短路径的顶点的路径，则记录
                cands.enqueue((plen + 1, vmin, v))
        count += 1
        # print(paths)
    return paths


# 确定出发点和最后的站点
def computefshortestpath(startpos, endpos):
    s1 = STATION_NUM[startpos]
    e1 = STATION_NUM[endpos]
    # print(s1,e1)
    paths = dijkstra_shortest_pathS(pathss, s1, e1)
    # print(paths)
    b = []
    p = paths[e1][0]
    # print(paths[e1])
    b.append(STATIO[p])
    while True:
        p1 = paths[p][0]
        p = p1
        b.append(STATIO[p])
        if p == s1:
            break
    b.reverse()
    b.append(STATIO[e1])

    s = ""
    s += b[0]
    for i in range(1, len(b) - 1):
        a1 = set(datanum[b[i - 1]])
        b1 = set(datanum[b[i + 1]])
        c1 = set(datanum[b[i]])
        # 如果没有交集，说明不是同一条路
        if not len(a1 & b1):
            if len(datanum[b[i + 1]]) != 0:
                s += "-" + str((list(set(datanum[b[i]]) & b1)[0])) + "号线"
            s += "-" + b[i]
        else:
            s += "-" + b[i]
    s += "-" + b[len(b) - 1]
    return b, s

if __name__ == "__main__":
    startpos = input()
    endpos = input()
    strpath, s = computefshortestpath(startpos,endpos)
    print(s)
    # print(getInfo())
