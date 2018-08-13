import numpy as np
from scipy.spatial import Delaunay
import math

#计算投影面积
#轮廓周长

def fun(vx, vy, vz, T):  #计算三维平面转二维平面
    old = np.mat([vx, vy, vz, 1])
    new = old * T
    res = new.getA()
    return [res[0][0], res[0][1]]


def gettransform(newy, newz):    #转置矩阵
    if (newy[2] * newz[0] - newy[0] * newz[2]) < 0.001:
        x = 0
        z = 0
    else:
        z = (newy[0] * newz[1] - newy[1] * newz[0]) / (newy[2] * newz[0] - newy[0] * newz[2])
        x = (newy[1] * newz[2] - newy[2] * newz[1]) / (newy[2] * newz[0] - newy[0] * newz[2])
    mod = np.sqrt(1 + x**2 + z**2)
    T = np.mat([[x/mod, 1/mod, z/mod, 0],
                [newy[0], newy[1], newy[2], 0],
                [newz[0], newz[1], newz[2], 0],
                [0, 0, 0, 1]])
    return T

def getcircum_r_area(simplice,propoint):
    a = propoint[simplice[0]]
    b = propoint[simplice[1]]
    c = propoint[simplice[2]]
    ab = np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)
    ac = np.sqrt((a[0]-c[0])**2+(a[1]-c[1])**2)
    bc = np.sqrt((b[0]-c[0])**2+(b[1]-c[1])**2)
    s = (ab + ac + bc) / 2.0
    area = np.sqrt(s*(s-ab)*(s-ac)*(s-bc))
    circum_r = ab*ac*bc/(4.0*area)
    return circum_r, area

def getarea(a, b, c):  #计算面片面积
    ab = np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    ac = np.sqrt((a[0] - c[0]) ** 2 + (a[1] - c[1]) ** 2)
    bc = np.sqrt((b[0] - c[0]) ** 2 + (b[1] - c[1]) ** 2)
    s = (ab + ac + bc) / 2.0
    area = np.sqrt(s * (s - ab) * (s - ac) * (s - bc))
    return area

class A1:
    def __init__(self, obj, vpoint, head):
        self.obj = obj
        self.core = [0, 0, 0]  # 图形中心
        self.head = head       # 头朝向
        self.propoint = []     #二维散点坐标
        self.prosurface = vpoint
        self.newindex = []
        self.Are = []          #视点熵的上面
        self.T = 0             #转置矩阵
        self.proPoint()
        self.area = 0          #投影面积
        self.cir = 0           #投影周长
        self.shan = 0          #熵
        self.getShadowArea()
        self.getlenth()
        self.getshannon()

    def proPoint(self):
        face = []
        for row in self.obj.faces:
            face.append(row[0])
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
            self.propoint.append(fun(vx1, vy1, vz1, self.T))
            vx2 = visVertices[v2index][0]
            vy2 = visVertices[v2index][1]
            vz2 = visVertices[v2index][2]
            self.propoint.append(fun(vx2, vy2, vz2, self.T))
            vx3 = visVertices[v3index][0]
            vy3 = visVertices[v3index][1]
            vz3 = visVertices[v3index][2]
            self.propoint.append(fun(vx3, vy3, vz3, self.T))

    def drawDelaunay(self):

        self.point = np.array(self.propoint)
        tri = Delaunay(self.point)
        self.index = tri.simplices.copy()
        self.concavehull()

    def getShadowArea(self):
        self.drawDelaunay()
        for i in self.newindex:
            self.area += getarea(self.point[i[0]], self.point[i[1]], self.point[i[2]])
        #print("投影面积")
        #print(self.area)

        #plt.title("concave hull")
        #plt.triplot(point[:, 0], point[:, 1], self.newindex)
        #plt.triplot(point[:, 0], point[:, 1], self.index)
        #plt.plot(point[:, 0], point[:, 1], ',')
        #plt.show()

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

    def getshannon(self):
        for curA in self.Are:
            p = curA/self.area   #概率
            self.shan += - p * math.log(p, 2)