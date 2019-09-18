# coding=utf-8
# 基于邻接表定义图，继承图类，也可以直接写
from GraphError import GraphError
from Graph import Graph
class GraphAL(Graph):
    def __init__(self, mat=None, unconn=0):
        if mat is None:
            mat = []
        vnum=len(mat)
        for x in mat:
            if len(x)!=vnum:
                raise ValueError("Argument for 'GraphAL'.")
        self._mat=[Graph._out_edges(mat[i], unconn) for i in range(vnum)]
        self._vnum=vnum
        self._unconn=unconn
    def add_vertex(self):#增加新节点时安排一个新编号
        self._mat.append([])
        self._vnum+=1
        return self._vnum-1
    def add_edge(self,vi,vj,val=1):
        if self._vnum==0:
            raise GraphError("cannot add edge to empty graph")
        if self._invalid(vi) or self._invalid(vj):
            raise GraphError(str(vi) + ' or ' + str(vj) + " is not a valid vertex.")
        row=self._mat[vi]
        i=0
        while i<len(row):
            if row[i][0]==vj:#更新mat[vi][vj]的值
                self._mat[vi][i]=(vj,val)
                return
            if row[i][0]>vj:#原来如果没有到vj的边，退出循环，加入边
                break
            i+=1
        self._mat[vi].insert(i,(vj,val))
    def get_edge(self,vi,vj):
        if self._invalid(vi) or self._invalid(vj):
            raise GraphError(str(vi) + ' or ' + str(vj) + " is not a valid vertex.")
        for i,val in self._mat[vi]:
            if i==vj:
                return val
        return self._unconn
    def out_edges(self,vi):
        if self._invalid(vi):
            raise GraphError(str(vi) + " is not a valid vertex.")
        return self._mat[vi]
