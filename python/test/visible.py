# -*- coding: utf-8 -*-
import numpy as np

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
def funVisible1(obj, vpnormal):
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

    for i in face:
        for j in i:
            unvisiblevid.append(j)

    unvisiblev = list(set(unvisiblevid))
    index = 0
    flag = 0
    for i in range(len(unvisiblev)-1, -1, -1):
        t = unvisiblev[i] - 1
        flag = 0
        for cur in range(index, len(face), 2):
            v1index = face[cur][0] - 1
            v2index = face[cur][1] - 1
            v3index = face[cur][2] - 1
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
            if (s1 > 0 and s2 > 0 and s3 > 0) or (s1 < 0 and s2 < 0 and s3 < 0):
                L2 = plucker(vpnormal, v0)
                L3 = plucker(v0, visVertices[t])
                L4 = plucker(v1, v2)
                s4 = sideOp(L4, L3)
                s5 = sideOp(L4, L2)

                if s4 * s5 > 0:
                    del unvisiblev[i]
                    index = cur
                    flag = 1
                    break
        if flag == 1:
            continue
        for cur in range(index-1, -1, -2):
            v1index = face[cur][0] - 1
            v2index = face[cur][1] - 1
            v3index = face[cur][2] - 1
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
            if (s1 > 0 and s2 > 0 and s3 > 0) or (s1 < 0 and s2 < 0 and s3 < 0):
                L2 = plucker(vpnormal, v0)
                L3 = plucker(v0, visVertices[t])
                L4 = plucker(v1, v2)
                s4 = sideOp(L4, L3)
                s5 = sideOp(L4, L2)

                if s4 * s5 > 0:
                    del unvisiblev[i]
                    index = cur
                    break
    isExist = np.in1d(face, unvisiblev)
    cnt = 0
    for i in range(len(face)-1, -1, -1):
        if isExist[i*3] == False or isExist[i*3+1] == False or isExist[i*3+2] == False:
            cnt += 1
            del face[i]
    print(cnt)
    return face




def funVisible2(obj, vpnormal):
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

    for i in face:
        for j in i:
            unvisiblevid.append(j)

    unvisiblev = list(set(unvisiblevid))

    for i in range(len(unvisiblev)-1, -1, -1):
        t = unvisiblev[i] - 1

        for j in face:
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
            if (s1 > 0 and s2 > 0 and s3 > 0) or (s1 < 0 and s2 < 0 and s3 < 0):
                L2 = plucker(vpnormal, v0)
                L3 = plucker(v0, visVertices[t])
                L4 = plucker(v1, v2)
                s4 = sideOp(L4, L3)
                s5 = sideOp(L4, L2)

                if s4 * s5 > 0:
                    del unvisiblev[i]
                    break
    isExist = np.in1d(face, unvisiblev)
    cnt = 0
    for i in range(len(face)-1, -1, -1):
        if isExist[i*3] == False or isExist[i*3+1] == False or isExist[i*3+2] == False:
            cnt += 1
            del face[i]
    print(cnt)
    return face
