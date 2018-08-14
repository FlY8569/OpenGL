import numpy as np


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

def getZhongxin(a, b, c):  #计算重心
    x = (a[0] + b[0] + c[0]) / 3
    y = (a[1] + b[1] + c[1]) / 3
    z = (a[2] + b[2] + c[2]) / 3
    zhongxin = [x, y, z]
    return zhongxin


def distance(zhongxin, vpoint):  #计算距离
    dis = np.sqrt((zhongxin[0] - vpoint[0]) ** 2 + (zhongxin[1] - vpoint[1]) ** 2 + (zhongxin[2] - vpoint[2]) ** 2)
    return dis

#plucker坐标
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



def visible(obj, vpnormal):  #计算可见面
    m = 0
    face = obj.faces[:]
    visVertices = obj.vertices[:]
    unvisiblevid = []  # 所有可见点的集合
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
    print(len(face))
    for i in face:
        for j in i:
            unvisiblevid.append(j)

    unvisiblev = list(set(unvisiblevid))
    cnt = 0
    x = 0
    for i in range(len(unvisiblev)-1, -1, -1):
        t = unvisiblev[i] - 1
        x = x + 1
        c = 0
        for j in obj.faces:
            c = c + 1
            v1index = j[0] - 1
            v2index = j[1] - 1
            v3index = j[2] - 1
            if t == v1index or t == v2index or t == v3index:
                continue
            vx1 = visVertices[v1index][0]
            vy1 = visVertices[v1index][1]
            vz1 = visVertices[v1index][2]
            vx2 = visVertices[v2index][0]
            vy2 = visVertices[v2index][1]
            vz2 = visVertices[v2index][2]
            vx3 = visVertices[v3index][0]
            vy3 = visVertices[v3index][1]
            vz3 = visVertices[v3index][2]
            v0 = (vx1, vy1, vz1)
            v1 = (vx2, vy2, vz2)
            v2 = (vx3, vy3, vz3)
            e1 = plucker(v1, v0)
            e2 = plucker(v2, v1)
            e3 = plucker(v0, v2)
            L = plucker(vpnormal, visVertices[t])
            s1 = sideOp(L, e1)
            s2 = sideOp(L, e2)
            s3 = sideOp(L, e3)
            # if c == 4425:
            #     print("vpnormal" + str(vpnormal) + "visVertices[t]" + str(visVertices[t]))
            #     print(v0)
            #     print(v1)
            #     print(v2)
            #     print(" s1  " + str(s1) + "  s2  " + str(s2) + "  s3  " + str(s3))
            if (s1 > 0 and s2 > 0 and s3 > 0) or (s1 < 0 and s2 < 0 and s3 < 0):
                L2 = plucker(vpnormal, v0)
                L3 = plucker(v0, visVertices[t])
                L4 = plucker(v1, v2)
                s4 = sideOp(L4, L3)
                s5 = sideOp(L4, L2)
                # print("  s4  " + str(s4) + "  s5  " + str(s5))

                if s4 * s5 > 0:
                    print(c , x)
                    del unvisiblev[i]
                    cnt = cnt + 1
                    break
    isExist = np.in1d(face, unvisiblev)
    print("cnt")
    print(cnt)
    for i in range(len(face)-1, -1, -1):
        if isExist[i*3] == False or isExist[i*3+1] == False or isExist[i*3+2] == False:
            del face[i]
    print(len(face))
    print("is done")
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