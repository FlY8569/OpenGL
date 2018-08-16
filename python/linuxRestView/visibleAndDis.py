import numpy as np


# 计算可见面
# 计算表面可见度
# 计算模型在当前视角下的最大深度

def getCenterGravity(a, b, c):  #计算重心
    x = (a[0] + b[0] + c[0]) / 3
    y = (a[1] + b[1] + c[1]) / 3
    z = (a[2] + b[2] + c[2]) / 3
    centerGravity = [x, y, z]
    return centerGravity


def distance(centerGravity, viewPoint):  #计算距离
    dis = np.sqrt((centerGravity[0] - viewPoint[0]) ** 2 + (centerGravity[1] - viewPoint[1]) ** 2 + (centerGravity[2] - viewPoint[2]) ** 2)
    return dis

# plucker坐标
def plucker(a, b):
    l0 = a[0] * b[1] - b[0] * a[1]
    l1 = a[0] * b[2] - b[0] * a[2]
    l2 = a[0] - b[0]
    l3 = a[1] * b[2] - b[1] * a[2]
    l4 = a[2] - b[2]
    l5 = b[1] - a[1]
    return [l0, l1, l2, l3, l4, l5]
def sideOp(a, b):
    res = a[0] * b[4] + a[1] * b[5] + a[2] * b[3] + a[3] * b[2] + a[4 ] * b[0] + a[5] * b[1]
    return res
# 求所有可见面
def funVisible(obj, vpnormal):
    m = 0
    face = obj.faces[:]
    unvisiblevid = []  # 所有可见点的集合
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

    # for i in face:
    #     for j in i:
    #         unvisiblevid.append(j)
    #
    # unvisiblev = list(set(unvisiblevid))
    # cnt = 0
    # for i in range(len(unvisiblev)-1, -1, -1):
    #     t = unvisiblev[i] - 1
    #
    #     for j in obj.faces:
    #         v1index = j[0] - 1
    #         v2index = j[1] - 1
    #         v3index = j[2] - 1
    #         if t == v1index or t == v2index or t == v3index:
    #             continue
    #         vx1 = visVertices[v1index][0]
    #         vy1 = visVertices[v1index][1]
    #         vz1 = visVertices[v1index][2]
    #         vx2 = visVertices[v2index][0]
    #         vy2 = visVertices[v2index][1]
    #         vz2 = visVertices[v2index][2]
    #         vx3 = visVertices[v3index][0]
    #         vy3 = visVertices[v3index][1]
    #         vz3 = visVertices[v3index][2]
    #         v0 = (vx1, vy1, vz1)
    #         v1 = (vx2, vy2, vz2)
    #         v2 = (vx3, vy3, vz3)
    #         e1 = plucker(v1, v0)
    #         e2 = plucker(v2, v1)
    #         e3 = plucker(v0, v2)
    #         L = plucker(vpnormal, visVertices[t])
    #         s1 = sideOp(L, e1)
    #         s2 = sideOp(L, e2)
    #         s3 = sideOp(L, e3)
    #         #     print("vpnormal" + str(vpnormal) + "visVertices[t]" + str(visVertices[t]))
    #         #     print(v0)
    #         #     print(v1)
    #         #     print(v2)
    #         #     print(" s1  " + str(s1) + "  s2  " + str(s2) + "  s3  " + str(s3))
    #         if (s1 > 0 and s2 > 0 and s3 > 0) or (s1 < 0 and s2 < 0 and s3 < 0):
    #             L2 = plucker(vpnormal, v0)
    #             L3 = plucker(v0, visVertices[t])
    #             L4 = plucker(v1, v2)
    #             s4 = sideOp(L4, L3)
    #             s5 = sideOp(L4, L2)
    #             # print("  s4  " + str(s4) + "  s5  " + str(s5))
    #
    #             if s4 * s5 > 0:
    #                 del unvisiblev[i]
    #                 cnt = cnt + 1
    #                 break
    # isExist = np.in1d(face, unvisiblev)
    # print("cnt")
    # print(cnt)
    # for i in range(len(face)-1, -1, -1):
    #     if isExist[i*3] == False or isExist[i*3+1] == False or isExist[i*3+2] == False:
    #         del face[i]
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


class VisibleAndDis:
    def __init__(self, obj, vpoint):
        self.obj = obj
        self.viewPoint = vpoint.copy()        # 视点位置
        self.visface = None            # 所有可见面
        self.visarea = 0               # 所有可见面面积
        self.eyevisface = None         # 眼睛的可见面
        self.eyevisarea = 0            # 眼睛可见面积
        self.surfaceVisibility = 0     # 表面可见度
        self.eyeVisibility = 0         # 眼睛可见度
        self.dismin = 0x3f3f3f         # 距离
        self.getvisibleface()
        self.getVisibility()
        self.getEyeVis()

    def getvisibleface(self):
        self.visface = funVisible(self.obj, self.viewPoint)

    # 计算表面可见度和最大深度
    def getVisibility(self):
        for index in self.visface:
            self.visarea = self.visarea + getarea(self.obj.vertices[index[0] - 1], self.obj.vertices[index[1] - 1],
                                                  self.obj.vertices[index[2] - 1])
            zhongxin = getCenterGravity(self.obj.vertices[index[0] - 1], self.obj.vertices[index[1] - 1],
                                   self.obj.vertices[index[2] - 1])
            dis = distance(zhongxin, self.viewPoint)
            if self.dismin > dis:
                self.dismin = dis
        self.surfaceVisibility = self.visarea / self.obj.area

    def getEyeVis(self):
        self.eyevisface = eyeVisible(self.obj, self.visface)
        for index in self.eyevisface:
            self.eyevisarea = self.eyevisarea + getarea(self.obj.vertices[index[0] - 1], self.obj.vertices[index[1] - 1],
                                                  self.obj.vertices[index[2] - 1])
        self.eyeVisibility = self.eyevisarea / self.visarea