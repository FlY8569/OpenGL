import numpy as np
from OpenGL.GL import *
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt


def fun(core, prosurface, vx, vy, vz, T):  #计算三维平面转二维平面
    vpt = prosurface[0] * prosurface[0] + prosurface[1] * prosurface[1] + prosurface[2] * prosurface[2]
    t = ((core[0] - vx) * prosurface[0] + (core[1] - vy) * prosurface[1] + (core[2] - vz) * prosurface[2]) / vpt
    x = vx + prosurface[0] * t
    y = vy + prosurface[1] * t
    z = vz + prosurface[2] * t
    old = np.mat([x, y, z, 1])
    new = old * T
    res = new.getA()
    return [res[0][0], res[0][2]]


def gettransform(a, b, c, core, prosurface):    #转置矩阵
    if (b * prosurface[2] - c * prosurface[1]) < 0.01:
        y = 0
        z = 0
    else:
        y = (c * prosurface[0] - a * prosurface[2]) / (b * prosurface[2] - c * prosurface[1])
        z = (a * prosurface[1] - b * prosurface[0]) / (b * prosurface[2] - c * prosurface[1])
    x0 = -(core[0] * 1 + core[1] * y + core[2] * z)
    y0 = -(core[0] * a + core[1] * b + core[2] * c)
    z0 = -(core[0] * prosurface[0] + core[1] * prosurface[1] + core[2] * prosurface[2])
    T = np.mat([[1, y, z, x0],
                [a, b, c, y0],
                [prosurface[0], prosurface[1], prosurface[2], z0],
                [0, 0, 0, 1]])
    return T

def getlen(simplice,propoint):
    a = propoint[simplice[0]]
    b = propoint[simplice[1]]
    c = propoint[simplice[2]]
    ab = ((a[0]-b[0])**2+(a[1]-b[1])**2) ** 0.5
    ac = ((a[0]-c[0])**2+(a[1]-c[1])**2) ** 0.5
    bc = ((b[0]-c[0])**2+(b[1]-c[1])**2) ** 0.5
    abc = [ab, ac, bc]
    return max(abc)
class A1:
    def __init__(self, obj, vpoint, head):
        self.obj = obj
        self.core = obj.bbox_center[:]  # 图形中心
        self.vp = vpoint  # 视点位置
        self.head = head  # 头朝向
        self.propoint = [] #二维散点坐标
        self.prosurface = np.array(
            [self.vp[0] - self.core[0], self.vp[1] - self.core[1], self.vp[2] - self.core[2]])  # 投影面法向量

    def proPoint(self):
        face = []
        for row in self.obj.faces:
            face.append(row[0])
        visVertices = self.obj.vertices[:]
        T = gettransform(self.head[0], self.head[1], self.head[2], self.core, self.prosurface)
        for i in range(len(face)):
            v1index = face[i][0] - 1
            v2index = face[i][1] - 1
            v3index = face[i][2] - 1
            vx1 = visVertices[v1index][0]
            vy1 = visVertices[v1index][1]
            vz1 = visVertices[v1index][2]
            self.propoint.append(fun(self.core, self.prosurface, vx1, vy1, vz1, T))
            vx2 = visVertices[v2index][0]
            vy2 = visVertices[v2index][1]
            vz2 = visVertices[v2index][2]
            self.propoint.append(fun(self.core, self.prosurface, vx2, vy2, vz2, T))
            vx3 = visVertices[v3index][0]
            vy3 = visVertices[v3index][1]
            vz3 = visVertices[v3index][2]
            self.propoint.append(fun(self.core, self.prosurface, vx3, vy3, vz3, T))

    def drawDelaunay(self):
        self.proPoint()
        point = np.array(self.propoint)
        tri = Delaunay(point)
        self.index = tri.simplices.copy()
        newindex = self.concavehull()
        plt.triplot(point[:, 0], point[:, 1], newindex)
        plt.plot(point[:, 0], point[:, 1], 'o')
        plt.show()

    def concavehull(self):
        zlen = []
        newindex = []
        for simplice in self.index:
            zlen.append(getlen(simplice, self.propoint))
        arrzlen = np.array(zlen)
        print(arrzlen)
        meanzlen = arrzlen.mean(axis=0)
        for i in range(len(zlen)-1, -1, -1):
            if(zlen[i] < meanzlen):
                newindex.append(self.index[i])
        return newindex


    def get_a1_list(self):
        self.a1_list = glGenLists(1)
        glNewList(self.a1_list, GL_COMPILE)
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_POINTS)
        for i in range(len(self.propoint)):
            glVertex2fv(self.propoint[i])
        glEnd()
        glEndList()
