import numpy as np
from scipy.spatial import Delaunay
from BestView.function import *
import math

# 计算投影面积
# 轮廓周长
# 计算可见面
# 计算表面可见度
# 计算模型在当前视角下的最大深

class Attribute:
    def __init__(self, obj, vpoint, head):
        self.vp = vpoint.copy()  # 视点位置
        self.obj = obj
        self.core = [0, 0, 0]  # 图形中心
        self.head = head.copy()       # 头朝向
        self.propoint = []     #二维散点坐标
        self.prosurface = vpoint.copy()
        self.newindex = []
        self.Are = []          #视点熵的上面
        self.T = 0             #转置矩阵
        self.proPoint()
        self.area = 0          #投影面积
        self.cir = 0           #投影周长
        self.shan = 0          #熵

        self.core = obj.bbox_center[:]  # 图形中心
        self.visface = None  # 所有可见面
        self.visarea = 0  # 所有可见面面积
        self.eyevisface = None  # 眼睛的可见面
        self.eyevisarea = 0  # 眼睛可见面积
        self.surfaceVisibility = 0  # 表面可见度
        self.eyeVisibility = 0
        self.dismin = 0x3f3f3f

        #self.getShadowArea()
        #self.getlenth()
        #self.getshannon()

        self.getvisibleface()
        #self.getVisibility()
        #self.getEyeVis()

    def proPoint(self):
        face = self.obj.faces[:]
        visVertices = self.obj.vertices[:]

        mod = np.sqrt(self.prosurface[0]**2 + self.prosurface[1]**2 + self.prosurface[2]**2)
        self.prosurface /= -mod   #z轴
        mod = np.sqrt(self.head[0]**2 + self.head[1]**2 + self.head[2]**2)
        self.head /= mod   #y轴
        self.T = gettransform(self.head, self.prosurface)

        for i in range(len(face)):
            v1index = face[i][0] - 1
            v2index = face[i][1] - 1
            v3index = face[i][2] - 1
            vx1 = visVertices[v1index][0]
            vy1 = visVertices[v1index][1]
            vz1 = visVertices[v1index][2]
            t1 = fun(vx1, vy1, vz1, self.T)
            self.propoint.append(t1)
            vx2 = visVertices[v2index][0]
            vy2 = visVertices[v2index][1]
            vz2 = visVertices[v2index][2]
            t2 = fun(vx2, vy2, vz2, self.T)
            self.propoint.append(t2)
            vx3 = visVertices[v3index][0]
            vy3 = visVertices[v3index][1]
            vz3 = visVertices[v3index][2]
            t3 = fun(vx3, vy3, vz3, self.T)
            self.propoint.append(t3)

    def drawDelaunay(self):

        self.point = np.array(self.propoint)
        tri = Delaunay(self.point)
        self.index = tri.simplices.copy()
        self.concavehull()

    def getShadowArea(self):  #计算投影面积
        self.drawDelaunay()
        for i in self.newindex:
            self.area += getarea(self.point[i[0]], self.point[i[1]], self.point[i[2]])

    def concavehull(self):
        cirR = []
        for simplice in self.index:
            r, ar = getcircum_r_area(simplice, self.propoint)
            cirR.append(r)
            self.Are.append(ar)
        arrcirR = np.array(cirR)
        meanr = arrcirR.mean(axis=0)
        for i in range(len(cirR)-1, -1, -1):
            if(cirR[i] < meanr * 2):     #参数设置 : 多大的边要被筛掉
                self.newindex.append(self.index[i])


    def getlenth(self):  #计算投影周长
        dirindex = {}
        lenindex = []
        for i in self.newindex:
            i.sort()
            if (i[0], i[1]) in dirindex.keys():
                dirindex[(i[0], i[1])] += 1
            else:
                dirindex[(i[0], i[1])] = 1
            if (i[0], i[2]) in dirindex.keys():
                dirindex[(i[0], i[2])] += 1
            else:
                dirindex[(i[0], i[2])] = 1
            if (i[1], i[2]) in dirindex.keys():
                dirindex[(i[1], i[2])] += 1
            else:
                dirindex[(i[1], i[2])] = 1
        for key in dirindex:
            if dirindex[key] == 1:
                lenindex.append(key)
                a = self.propoint[key[0]][0] - self.propoint[key[1]][0]
                b = self.propoint[key[0]][1] - self.propoint[key[1]][1]
                self.cir += np.sqrt(a ** 2 + b ** 2)

    def getshannon(self):  #计算香农熵
        for curA in self.Are:
            p = curA/self.area   #概率
            self.shan += - p * math.log(p, 2)

    def getvisibleface(self):  #得到可见面
        self.visface = visible(self.obj, self.vp)

    def getVisibility(self):  # 计算表面可见度和最大深度
        for index in self.visface:
            self.visarea = self.visarea + getarea(self.obj.vertices[index[0] - 1], self.obj.vertices[index[1] - 1],
                                                  self.obj.vertices[index[2] - 1])
            zhongxin = getZhongxin(self.obj.vertices[index[0] - 1], self.obj.vertices[index[1] - 1],
                                   self.obj.vertices[index[2] - 1])
            dis = distance(zhongxin, self.vp)
            if (self.dismin > dis):
                self.dismin = dis

        self.surfaceVisibility = self.visarea / self.obj.area


    def getEyeVis(self):  #计算眼睛可见度
        self.eyevisface = eyeVisible(self.obj, self.visface)
        for index in self.eyevisface:
            self.eyevisarea = self.eyevisarea + getarea(self.obj.vertices[index[0] - 1], self.obj.vertices[index[1] - 1],
                                                  self.obj.vertices[index[2] - 1])
        self.eyeVisibility = self.eyevisarea / self.visarea