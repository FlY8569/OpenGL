import numpy as np
from OpenGL.GL import *


# 计算可见面
# 计算表面可见度
# 计算模型在当前视角下的最大深度

def getZhongxin(a, b, c):  #计算重心
    x = (a[0] + b[0] + c[0]) / 3
    y = (a[1] + b[1] + c[1]) / 3
    z = (a[2] + b[2] + c[2]) / 3
    zhongxin = [x, y, z]
    return zhongxin


def distance(zhongxin, vpoint):  #计算距离
    dis = np.sqrt((zhongxin[0] - vpoint[0]) ** 2 + (zhongxin[1] - vpoint[1]) ** 2 + (zhongxin[2] - vpoint[2]) ** 2)
    return dis


def sameside(A, B, C, P):
    ab = np.array([A[0] - B[0], A[1] - B[1], A[2] - B[2]])
    ac = np.array([C[0] - A[0], C[1] - A[1], C[2] - A[2]])
    ap = np.array([P[0] - A[0], P[1] - A[1], P[2] - A[2]])
    v1 = np.cross(ab, ac)
    v2 = np.cross(ab, ap)
    if np.dot(v1, v2) > 0:
        return True
    return False


def visible(obj, vpnormal):
    m = 0
    face = []
    for row in obj.faces:
        face.append(row[0])
    visVertices = obj.vertices[:]
    for i in range(len(face)):
        v1index = face[m][0] - 1
        v2index = face[m][1] - 1
        v3index = face[m][2] - 1
        vx1 = visVertices[v1index][0]
        vy1 = visVertices[v1index][1]
        vz1 = visVertices[v1index][2]
        vx2 = visVertices[v2index][0]
        vy2 = visVertices[v2index][1]
        vz2 = visVertices[v2index][2]
        vx3 = visVertices[v3index][0]
        vy3 = visVertices[v3index][1]
        vz3 = visVertices[v3index][2]
        a = (vy1 - vy2) * (vz1 - vz3) - (vy1 - vy3) * (vz1 - vz2)
        b = (vz1 - vz2) * (vx1 - vx3) - (vx1 - vx2) * (vz1 - vz3)
        c = (vx1 - vx2) * (vy1 - vy3) - (vx1 - vx3) * (vy1 - vy2)
        curnormal = np.array([a, b, c])

        if np.dot(vpnormal, curnormal) <= 0:
            del face[m]
            m = m - 1
        m = m + 1
        #
    for k in range(len(face) - 1, -1, -1):
        cnt = 0
        for i in face[k]:
            vx = visVertices[i - 1][0]
            vy = visVertices[i - 1][1]
            vz = 0
            p = [vx, vy, vz]
            for j in face:
                v1index = j[0] - 1
                v2index = j[1] - 1
                v3index = j[2] - 1
                if v1index == i or v2index == i or v3index == i:
                    break
                vx1 = visVertices[v1index][0]
                vy1 = visVertices[v1index][1]
                vz1 = 0
                vx2 = visVertices[v2index][0]
                vy2 = visVertices[v2index][1]
                vz2 = 0
                vx3 = visVertices[v3index][0]
                vy3 = visVertices[v3index][1]
                vz3 = 0
                a = [vx1, vy1, vz1]
                b = [vx2, vy2, vz2]
                c = [vx3, vy3, vz3]
                if sameside(a, b, c, p) and sameside(b, c, a, p) and sameside(c, a, b, p):
                    arrz = visVertices[v1index][2] + visVertices[v2index][2] + visVertices[v3index][2]
                    if visVertices[i - 1][2] <= arrz / 3:
                        cnt = cnt + 1
        if cnt > 1:
            del face[k]
    return face

def eyeVisible(obj, visface): #眼睛的可见面
    eyevisface = []
    for eyeface in obj.eye:
        e1 = eyeface[0]
        e2 = eyeface[1]
        e3 = eyeface[2]
        for objface in visface:
            v1 = objface[0]
            v2 = objface[1]
            v3 = objface[2]
            if e1 == v1 and e2 == v2 and e3 == v3:
                eyevisface.append(eyeface)
                break
    return eyevisface


# 计算3d 面片面积
def getarea(a, b, c):
    ab = np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)
    ac = np.sqrt((a[0] - c[0]) ** 2 + (a[1] - c[1]) ** 2 + (a[2] - c[2]) ** 2)
    bc = np.sqrt((b[0] - c[0]) ** 2 + (b[1] - c[1]) ** 2 + (b[2] - c[2]) ** 2)
    s = (ab + ac + bc) / 2.0
    area = np.sqrt(s * (s - ab) * (s - ac) * (s - bc))
    return area


class A2:
    def __init__(self, obj, vpoint):
        self.obj = obj
        self.core = obj.bbox_center[:]  # 图形中心
        self.vp = vpoint          # 视点位置
        self.visface = None      #所有可见面
        self.visarea = 0          #所有可见面面积
        self.eyevisface = None   #眼睛的可见面
        self.eyevisarea = 0      #眼睛可见面积
        self.surfaceVisibility = 0  # 表面可见度
        self.eyeVisibility = 0
        self.dismin = 0x3f3f3f
        self.getvisibleface()
        self.getVisibility()
        self.getEyeVis()

    def getvisibleface(self):
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
        #print(self.dismin)
        self.surfaceVisibility = self.visarea / self.obj.area
        #print("表面可见度")
        #print(self.surfaceVisibility)

    def getEyeVis(self):
        self.eyevisface = eyeVisible(self.obj, self.visface)
        for index in self.eyevisface:
            self.eyevisarea = self.eyevisarea + getarea(self.obj.vertices[index[0] - 1], self.obj.vertices[index[1] - 1],
                                                  self.obj.vertices[index[2] - 1])
        self.eyeVisibility = self.eyevisarea / self.visarea


    def get_a2_list(self):  # 显示可见面
        self.a2_list = glGenLists(1)
        glNewList(self.a2_list, GL_COMPILE)
        glColor3f(1.0, 1.0, 1.0)

        for face in self.visface:
            glBegin(GL_POLYGON)
            for i in range(len(face)):
                glVertex3fv(self.obj.vertices[face[i] - 1])
            glEnd()
        glEndList()
